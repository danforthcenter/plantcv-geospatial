# PlantCV-Geospatial class interactive georeferencer

import os
import napari
from magicgui.widgets import PushButton, Label, Container
from plantcv.plantcv import fatal_error, warn
from plantcv.geospatial._helpers import _read_raster
from plantcv.geospatial.write_geotif import write_geotif
from plantcv.geospatial.georeference import _transform_helpers as th

# Valid parameter lists.
_VALID_MODES = ("reference_image", "known_coordinates")
_VALID_TRANSFORMS = ("affine", "polynomial2", "polynomial3", "tps", "projective")
_VALID_IMAGE_EXTENSIONS = (".tif", ".tiff", ".TIF", ".TIFF")


class InteractiveGeoreferencer:
    """Plantcv-Geospatial interactive georeferencer class."""
    
    def __init__(self, img_dir, output_dir, mode="known_coordinates", known_coords=None,
                 reference_image=None, transform_type="affine",
                 interpolation_order=1, show=True):
        """Initialize parameters.

        Parameters
        ----------
        img_dir : str
            Directory containing the images to georeference.
        output_dir : str
            Directory that warped, georeferenced GeoTIFFs will be written into by
            `georeference()`. Created if it doesn't already exist.
        mode : str, optional
            "reference_image" or "known_coordinates". Default is "known_coordinates".
        known_coords : list of (float, float), optional
            Required when mode == "known_coordinates". Real-world (x, y)
            coordinates of the ground control points you will click on every
            image. 
        reference_image : str, optional
            Required (and only used) when mode == "reference_image". Path to the
            already-georeferenced image that other images will be aligned to.
        transform_type : str, optional
            "affine", "polynomial2", "polynomial3", "tps", or "projective".
            "polynomial2"/"polynomial3" are 2nd/3rd-order polynomial warps.
        interpolation_order : int, optional
            Pixel resampling interpolation degree used when warping (0=nearest
            neighbor, 1=bilinear, 3=bicubic). Default is 1.
        show : bool, optional
            Whether to display the napari viewer window. Default is True.
        """
        # Validate the mode-specific arguments first
        if mode not in _VALID_MODES:
            fatal_error(f"mode '{mode}' is not recognized. Must be one of {_VALID_MODES}.")
        if transform_type not in _VALID_TRANSFORMS:
            fatal_error(f"transform_type '{transform_type}' is not recognized. "
                        f"Must be one of {_VALID_TRANSFORMS}.")
        if mode == "known_coordinates" and (not known_coords or len(known_coords) < 3):
            fatal_error("mode='known_coordinates' requires `known_coords`, a list of at least "
                        "3 (x, y) real-world coordinate pairs.")
        if mode == "reference_image" and not reference_image:
            fatal_error("mode='reference_image' requires `reference_image`, the path to an "
                        "already-georeferenced image to align other images to.")

        min_pts = th.MIN_POINTS_REQUIRED[transform_type]
        if mode == "known_coordinates" and len(known_coords) < min_pts:
            fatal_error(f"transform_type='{transform_type}' needs at least {min_pts} points, "
                        f"but `known_coords` only has {len(known_coords)}.")

        # Build file list.
        candidate_paths = sorted(os.listdir(img_dir))
        target_paths = [os.path.join(img_dir, p) for p in candidate_paths
                        if os.path.splitext(p)[1].lower() in _VALID_IMAGE_EXTENSIONS]
        excluded_paths = [os.path.join(img_dir, p) for p in candidate_paths
                        if os.path.splitext(p)[1].lower() not in _VALID_IMAGE_EXTENSIONS]
        print(target_paths)
        if excluded_paths:
            warn(f"Ignoring {len(excluded_paths)} file(s) that don't end "
                 f"in {_VALID_IMAGE_EXTENSIONS}: "
                 + ", ".join(os.path.basename(p) for p in excluded_paths))
        if not target_paths:
            fatal_error(f"No {_VALID_IMAGE_EXTENSIONS} files were found "
                        f"in '{img_dir}'.")

        # Find reference image and put it first if necessary
        self.mode = mode
        if mode == "reference_image":
            reference_abspath = os.path.abspath(reference_image)
            target_paths = [p for p in target_paths if os.path.abspath(p) != reference_abspath]
            self._queue = [reference_image] + target_paths
            self._is_reference = [True] + [False] * len(target_paths)
        else:
            self._queue = target_paths
            self._is_reference = [False] * len(target_paths)

        # Configuration
        self.output_dir = output_dir
        self.known_coords = known_coords
        self.reference_image = reference_image
        self.transform_type = transform_type
        self.interpolation_order = interpolation_order

        # Filled in later by the first image read
        self.crs = None

        # Session state, updated live as the user clicks through images.
        # track gcp clicks per image
        self.gcps = {}
        # reference image points
        self.reference_points = None
        self.skipped = set()
        self.current_index = 0
        self.finished = False

        # Build the napari viewer and its docked control panel
        self.viewer = napari.Viewer(show=show, title="PlantCV Interactive Georeferencer")
        self._status_label = Label(value="")
        self._next_button = PushButton(text="Next Image ▶")
        self._skip_button = PushButton(text="Skip This Image")
        self._next_button.clicked.connect(self._on_next)
        self._skip_button.clicked.connect(self._on_skip)
        controls = Container(widgets=[self._status_label, self._next_button, self._skip_button])
        self.viewer.window.add_dock_widget(controls, area="right", name="Georeferencing controls")

        self._load_current()


    # Internal helpers driving the click-through state machine
    def _expected_point_count(self):
        """How many points the user is expected to click on the current image.

        Returns
        -------
        int or None
            Expected number of points either from known coords or ref image clicks.
        """
        if self.mode == "known_coordinates":
            return len(self.known_coords)
        
        if self.reference_points is not None:
            return len(self.reference_points)
        return None

    def _load_current(self):
        """Load the current queue image into the (reused) napari viewer"""
        path = self._queue[self.current_index]
        array, _, _, _ = _read_raster(path)
        display = th.make_display_array(array)

        # Replace layers rather than creating a fresh Viewer per image
        self.viewer.layers.clear()
        self.viewer.add_image(display, name=os.path.basename(path))
        self._points_layer = self.viewer.add_points(name="GCPs", size=max(display.shape[:2]) / 100)

        self._update_status_label()

    def _update_status_label(self, extra_message=None):
        """Refresh the on-screen status label with current progress and instructions.

        Parameters
        ----------
        extra_message : str, optional
            Warning messages if applicable.
        """
        path = self._queue[self.current_index]
        step = self.current_index + 1
        total = len(self._queue)
        expected = self._expected_point_count()

        min_pts = th.MIN_POINTS_REQUIRED[self.transform_type]
        if self._is_reference[self.current_index]:
            lines = [f"STEP {step}/{total} - REFERENCE IMAGE: {os.path.basename(path)}",
                     "Click landmark points you can recognize in every other image.",
                     f"(at least {min_pts} points)"]
        else:
            lines = [f"STEP {step}/{total}: {os.path.basename(path)}"]
            if expected is not None:
                lines.append(f"Click the SAME {expected} point(s), in the SAME order, as before.")
            else:
                lines.append(f"Click at least {min_pts} point(s).")

        if extra_message:
            lines.insert(0, extra_message)
        self._status_label.value = "\n".join(lines)

    def _on_skip(self):
        """Callback for the "Skip This Image" button."""
        path = self._queue[self.current_index]
        if self._is_reference[self.current_index]:
            self._update_status_label("Can't skip the reference image - it defines the point set.")
            return
        self.skipped.add(path)
        self._advance()

    def _on_next(self):
        """Callback for the "Next Image" button: validate, store, and advance."""
        clicked_xy = [(float(pt[1]), float(pt[0])) for pt in self._points_layer.data]
        path = self._queue[self.current_index]
        min_pts = th.MIN_POINTS_REQUIRED[self.transform_type]
        expected = self._expected_point_count()

        if self._is_reference[self.current_index]:
            if len(clicked_xy) < min_pts:
                self._update_status_label(f"Need at least {min_pts} points (got {len(clicked_xy)}).")
                return
            self.reference_points = clicked_xy
        else:
            if expected is not None and len(clicked_xy) != expected:
                self._update_status_label(f"Expected exactly {expected} point(s), got {len(clicked_xy)}.")
                return
            self.gcps[path] = clicked_xy

        self._advance()

    def _advance(self):
        """Move to the next image in the queue, or finish if that was the last one."""
        self.current_index += 1
        if self.current_index >= len(self._queue):
            self._finish()
        else:
            self._load_current()

    def _finish(self):
        """Disable the control panel and tell the user to call `georeference()`."""
        self.finished = True
        n_done = len(self.gcps)
        n_skipped = len(self.skipped)
        self._next_button.enabled = False
        self._skip_button.enabled = False
        self._status_label.value = (
            f"All done! {n_done} image(s) ready, {n_skipped} skipped.\n"
            "Call `.georeference()` on this object (in a new cell) to warp and "
            "save the output GeoTIFFs."
        )

    def close(self):
        """Close the napari viewer held by this object.
        """
        self.viewer.close()


    # Now, the real georeferencing after points are collected

    def georeference(self):
        """Fit transforms from the collected points and write warped, georeferenced
        GeoTIFFs to `output_dir`.

        Returns
        -------
        list of str
            Paths to the GeoTIFF files that were written, in the same order as
            the images were shown.

        """
        if not self.gcps:
            fatal_error("No ground control points have been collected yet - click through at least "
                        "one image and click 'Next Image' before calling georeference().")
        # calls for each possible mode
        if self.mode == "reference_image":
            return self._georeference_to_reference()
        return self._georeference_to_known_coordinates()

    def _georeference_to_reference(self):
        """Warp every clicked target image onto the reference image."""
        if self.reference_points is None:
            fatal_error("The reference image has not been clicked yet - it must be the first "
                        "image you click through.")

        ref_array, ref_crs, ref_transform, ref_nodata = _read_raster(self.reference_image)
        ref_shape = ref_array.shape[:2]
        if ref_crs is None:
            warn(f"Reference image '{self.reference_image}' has no CRS of its own - outputs will be "
                 "pixel-aligned to it but will NOT carry real-world coordinates.")

        written_paths = []
        for path, src_xy in self.gcps.items():
            image_array, _, _, image_nodata = _read_raster(path)
            fill_value = image_nodata if image_nodata is not None else ref_nodata

            warped = th.warp_to_grid(image_array, ref_shape, self.reference_points, src_xy,
                                     self.transform_type, self.interpolation_order, fill_value)

            out_path = os.path.join(self.output_dir,
                                    f"{os.path.splitext(os.path.basename(path))[0]}_georef.tif")
            write_geotif(out_path, warped, ref_transform, ref_crs, fill_value)
            written_paths.append(out_path)

        self._report_skipped()
        return written_paths

    def _georeference_to_known_coordinates(self):
        """Warp every clicked image onto its own output grid, using the shared
        `known_coords` GCPs. 
        """
        written_paths = []
        pixel_size = None
        for path, src_xy in self.gcps.items():
            image_array, image_crs, _, image_nodata = _read_raster(path)
            fill_value = 0 if image_nodata is None else image_nodata

            if self.crs is None:
                # First image processed: borrow its CRS for every output GeoTIFF,
                # since the user never supplies one explicitly for this mode.
                if image_crs is None:
                    fatal_error(f"'{path}' has no CRS in its own file metadata"
                                "- add one to the source file, or use "
                                "mode='reference_image' instead.")
                self.crs = image_crs

            if pixel_size is None:
                # Likewise, estimate the output resolution once (from this same
                # first image) and reuse it for every image after it.
                pixel_size = th.estimate_pixel_size(src_xy, self.known_coords)
                print(f"Auto-estimated output pixel size of {pixel_size:.4g} CRS units per pixel "
                      f"from '{os.path.basename(path)}'.")

            out_shape, out_transform, out_pixel_xy = th.build_output_grid(
                image_array.shape, src_xy, self.known_coords, self.transform_type, pixel_size)

            warped = th.warp_to_grid(image_array, out_shape, out_pixel_xy, src_xy,
                                     self.transform_type, self.interpolation_order, fill_value)

            out_path = os.path.join(self.output_dir, 
                                    f"{os.path.splitext(os.path.basename(path))[0]}_georef.tif")
            write_geotif(out_path, warped, out_transform, self.crs, fill_value)
            written_paths.append(out_path)

        self._report_skipped()
        return written_paths

    def _report_skipped(self):
        """Print a reminder of any images that were skipped and therefore have no
        output file, so it's obvious why the output count is smaller than expected.
        """
        if self.skipped:
            names = ", ".join(os.path.basename(p) for p in sorted(self.skipped))
            warn(f"{len(self.skipped)} image(s) were skipped and have no output file: {names}")
