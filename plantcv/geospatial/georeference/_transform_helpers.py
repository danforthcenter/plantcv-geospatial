# Helper functions for interactive georeferencer class
import numpy as np
from affine import Affine
from skimage.transform import (AffineTransform, PolynomialTransform, PiecewiseAffineTransform,
                               ProjectiveTransform, warp)
from plantcv.plantcv import fatal_error, warn


POLYNOMIAL_ORDERS = {
    "polynomial2": 2,
    "polynomial3": 3,
}

# Minimum number of points to attempt each transformation type.
MIN_POINTS_REQUIRED = {
    "affine": 3,
    "polynomial2": 6,
    "polynomial3": 10,
    "tps": 4,
    "projective": 4,
}

# Sanity ceiling on the output raster build_output_grid() will produce. 
MAX_OUTPUT_DIMENSION = 20_000  # pixels, per side (height or width alone)
MAX_OUTPUT_PIXELS = 100_000_000  # total pixels (height * width)


def _fit_point_transform(transform_type, src_xy, dst_xy):
    """Fit a point-to-point transform, used in TWO different directions by callers.

    Parameters
    ----------
    transform_type : str
        One of "affine", "polynomial2", "polynomial3", "tps", "projective". See
        the module docstring for what each of these means and how they differ.
    src_xy : array_like, shape (N, 2)
        "Where the transform is fit FROM." Depending on the caller, this is either
        real image pixel coordinates or the pixel coordinates of an output canvas.
    dst_xy : array_like, shape (N, 2)
        "Where the transform is fit TO." The transform T returned will satisfy
        T(src_xy[i]) ~= dst_xy[i] for every point i.

    Returns
    -------
    skimage.transform._geometric.GeometricTransform
        A fitted, callable transform object: `transform(points)` maps an (N, 2)
        array of points from src-space into dst-space.
    """
    src = np.asarray(src_xy, dtype=float)
    dst = np.asarray(dst_xy, dtype=float)

    if transform_type == "affine":
        tform = AffineTransform.from_estimate(src, dst)
    elif transform_type in POLYNOMIAL_ORDERS:
        tform = PolynomialTransform.from_estimate(src, dst, order=POLYNOMIAL_ORDERS[transform_type])
    elif transform_type == "tps":
        tform = PiecewiseAffineTransform.from_estimate(src, dst)
    elif transform_type == "projective":
        tform = ProjectiveTransform.from_estimate(src, dst)
    else:
        fatal_error(f"transform_type '{transform_type}' is not recognized. Must be one of "
                    "'affine', 'polynomial2', 'polynomial3', 'tps', or 'projective'.")
        return None

    if tform is None:
        # from_estimate() returns None (rather than raising) if the fit fails
        fatal_error("Could not fit a " + transform_type + " transform from the clicked points. "
                    "Try clicking more points, spreading them out more (avoid points that are "
                    "all in a line), or choosing a lower-order transform.")
    return tform


def estimate_pixel_size(src_xy, world_xy):
    """Estimate a sensible output pixel size (ground sample distance) from GCPs.

    Parameters
    ----------
    src_xy : array_like, shape (N, 2)
        Pixel coordinates clicked on the source image.
    world_xy : array_like, shape (N, 2)
        Corresponding real-world coordinates (same order as src_xy).

    Returns
    -------
    float
        Estimated pixel size, in the same linear units as world_xy's CRS
        (e.g. meters if world_xy is in a UTM projection).
    """
    tform = _fit_point_transform("affine", src_xy, world_xy)
    # tform.params is the 3x3 homogeneous matrix used by skimage's transforms
    linear_part = tform.params[:2, :2]
    pixel_size = float(np.sqrt(abs(np.linalg.det(linear_part))))
    if pixel_size <= 0:
        # Degenerate fit (e.g. collinear points) - fall back to 1
        warn("Could not automatically estimate an output pixel size from the clicked points "
             "(they may be collinear). Defaulting to 1.0 - consider passing `resolution` "
             "explicitly to `georeference()` instead.")
        return 1.0
    return pixel_size


def build_output_grid(image_shape, src_xy, world_xy, transform_type, pixel_size):
    """Determine output raster grid that will contain an entire warped image.

    Parameters
    ----------
    image_shape : tuple
        (height, width) (or (height, width, bands)) of the SOURCE image being
        georeferenced.
    src_xy : array_like, shape (N, 2)
        Pixel coordinates clicked on the source image (same order as world_xy).
    world_xy : array_like, shape (N, 2)
        Known real-world coordinates for those same points.
    transform_type : str
        One of "affine", "polynomial2", "polynomial3", "tps", "projective".
    pixel_size : float
        Desired output pixel size (world units per pixel). The output grid is
        always built "north up" (rows increase downward/southward), matching the
        usual GeoTIFF convention.

    Returns
    -------
    out_shape : tuple of int
        (height, width) of the output raster that will contain the whole warped image.
    out_transform : affine.Affine
        Affine transform mapping output pixel (col, row) -> world (x, y)
    """
    height, width = image_shape[0], image_shape[1]
    corners_px = np.array([
        [0, 0],
        [width - 1, 0],
        [0, height - 1],
        [width - 1, height - 1],
    ], dtype=float)

    # Forward fit: pixel -> world.
    forward = _fit_point_transform(transform_type, src_xy, world_xy)
    corners_world = forward(corners_px)

    min_x, min_y = corners_world.min(axis=0)
    max_x, max_y = corners_world.max(axis=0)

    if not np.all(np.isfinite([min_x, min_y, max_x, max_y])):
        # int(np.ceil(...)) below would crash outright on inf/nan (OverflowError/
        # ValueError) rather than raise a clear message, so catch it here first.
        fatal_error(
            f"Fitting a '{transform_type}' transform and projecting the image corners through it "
            "produced non-finite world coordinates. The clicked points are likely too few, "
            "clustered, or nearly collinear for a stable fit - try clicking more, better-spread "
            "points, or a lower-order transform_type (e.g. 'affine' instead of 'polynomial2'/"
            "'polynomial3')."
        )

    # Guard against a degenerate bounding box
    out_width = max(1, int(np.ceil((max_x - min_x) / pixel_size)))
    out_height = max(1, int(np.ceil((max_y - min_y) / pixel_size)))

    if (out_width > MAX_OUTPUT_DIMENSION or out_height > MAX_OUTPUT_DIMENSION
            or out_width * out_height > MAX_OUTPUT_PIXELS):
        # Same root cause as the non-finite check above, just a less extreme
        # (but still nonsensical) degree of extrapolation - a bad fit doesn't
        # always blow up to infinity, sometimes "just" to an output raster no
        # one actually wants to allocate.
        fatal_error(
            f"Computed output raster would be {out_height} x {out_width} pixels, which exceeds "
            f"the sanity limit of {MAX_OUTPUT_DIMENSION:,}px per side / {MAX_OUTPUT_PIXELS:,} "
            f"- try clicking more, better-spread points, or a lower-order transform_type."
        )

    # North-up affine: pixel (0, 0) sits at the top-left = (min_x, max_y)
    out_transform = Affine.translation(min_x, max_y) * Affine.scale(pixel_size, -pixel_size)
    # `~out_transform` is the matrix inverse of the affine
    inverse = ~out_transform
    out_pixels = np.array([inverse * (float(x), float(y)) for x, y in world_xy])

    return (out_height, out_width), out_transform, out_pixels


def warp_to_grid(image_array, out_shape, out_pixel_xy, src_pixel_xy, transform_type,
                  interpolation_order, nodata_value):
    """Resample (warp) a source image array onto a destination pixel grid, given
    point correspondences between the two.

    Parameters
    ----------
    image_array : numpy.ndarray
        Source image data, shape (H, W) or (H, W, bands).
    out_shape : tuple of int
        (height, width) of the destination grid.
    out_pixel_xy : array_like, shape (N, 2)
        Pixel (x, y) coordinates, IN THE DESTINATION GRID, of the same N landmarks
        represented by src_pixel_xy (same order).
    src_pixel_xy : array_like, shape (N, 2)
        Pixel (x, y) coordinates clicked on the SOURCE image.
    transform_type : str
        One of "affine", "polynomial2", "polynomial3", "tps", "projective".
    interpolation_order : int
        Interpolation degree passed to skimage.transform.warp (0=nearest,
        1=bilinear, 3=bicubic, etc).
    nodata_value : float or None
        Value to fill in output pixels that fall outside the source image's
        footprint. If None, 0 is used.

    Returns
    -------
    numpy.ndarray
        Warped image, same dtype as `image_array`, shape (out_height, out_width)
        or (out_height, out_width, bands).
    """
    # inverse mapping as scikit expects
    inverse_map = _fit_point_transform(transform_type, out_pixel_xy, src_pixel_xy)

    fill_value = 0.0 if nodata_value is None else float(nodata_value)
    original_dtype = image_array.dtype

    # preserve_range=True stops skimage from rescaling pixel values into [0, 1]
    warped = warp(image_array, inverse_map, output_shape=out_shape, order=interpolation_order,
                  mode="constant", cval=fill_value, preserve_range=True)

    # Cast back to original image dtype
    if np.issubdtype(original_dtype, np.integer):
        info = np.iinfo(original_dtype)
        return np.clip(np.round(warped), info.min, info.max).astype(original_dtype)
    return warped.astype(original_dtype)


def make_display_array(array):
    """Build a small uint8 image suitable for showing in a napari viewer

    Parameters
    ----------
    array : numpy.ndarray
        Shape (H, W) or (H, W, bands), any dtype.

    Returns
    -------
    numpy.ndarray
        uint8 array, shape (H, W) or (H, W, 3), safe to pass to
        `napari.Viewer.add_image`.
    """
    if array.ndim == 2:
        return _stretch_to_uint8(array)

    n_bands = array.shape[-1]
    if n_bands == 1:
        return _stretch_to_uint8(array[:, :, 0])

    # Only the first 3 bands are used for display
    return np.dstack([_stretch_to_uint8(array[:, :, i]) for i in range(3)])


def _stretch_to_uint8(band, low_percentile=2, high_percentile=98):
    """Percentile-stretch a band for display.

    Parameters
    ----------
    band : numpy.ndarray
        2D array of any numeric dtype.
    low_percentile : float, optional
        Lower percentile clipped to 0. Default is 2.
    high_percentile : float, optional
        Upper percentile clipped to 255. Default is 98.

    Returns
    -------
    numpy.ndarray
        uint8 array, same shape as `band`.
    """
    finite = band[np.isfinite(band)]
    if finite.size == 0:
        return np.zeros_like(band, dtype=np.uint8)
    low, high = np.percentile(finite, [low_percentile, high_percentile])
    if high <= low:
        # Flat/uniform band - avoid a divide-by-zero, just show it as mid-gray.
        return np.full(band.shape, 128, dtype=np.uint8)
    stretched = np.clip((band.astype(float) - low) / (high - low), 0, 1) * 255
    return stretched.astype(np.uint8)
