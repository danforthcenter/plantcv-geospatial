# PlantCV-Geospatial classes

import napari
from plantcv.plantcv import fatal_error
from plantcv.geospatial.create_shapes.napari_grid import _napari_grid
from plantcv.geospatial.create_shapes.napari_polygon_grid import _napari_polygon_grid
from plantcv.geospatial.convert.points import points


class InteractiveShapes:
    """Plantcv-Geospatial interactive shapes class."""

    def __init__(self, img, viewer_type="napari", field_layer="field_boundary", show=True):
        """Initialize parameters.

        Parameters
        ----------
        viewer : str
            Type of viewer to initialize. Defaults to "napari".
        img : plantcv.plantcv.classes.Spectral_data
            Image to add to the first layer in an initialized viewer. Defaults to None.
        field_layer : str
            Name to call the first added shapes layer. Defaults to "field_boundary".
        """
        self.device = 0
        if viewer_type == "napari":
            self.viewer = napari.Viewer(show=show)
        else:
            fatal_error("Only napari viewers are currently supported.")

        self.img = img
        self.layer_dict = {}
        self.viewer.add_image(img.pseudo_rgb)
        self.viewer.add_shapes(name=field_layer)
        self.layer_dict["field_boundary"] = field_layer

    def add_layer(self, layer_type="shapes", layer_name="Shapes"):
        """Add a layer to the viewer.

        Parameters
        ----------
        layer_type : str, optional
            Type of layer to add. Options are "shapes" or "points". Defaults to "shapes".
        layer_name : str, optional
            Name of added layer. Defaults to "Shapes".
        """
        if layer_type == "shapes":
            self.viewer.add_shapes(name=layer_name)
            self.layer_dict["shapes_"+str(self.device)] = layer_name
            self.device += 1
        elif layer_type == "points":
            self.viewer.add_points(name=layer_name)
            self.layer_dict["points_"+str(self.device)] = layer_name
            self.device += 1
        else:
            fatal_error(f"Layer type {layer_type} is not supported. Layer_type must be 'shapes' or 'points'.")

    def grid(self, numdivs):
        """Add layers with lines forming a grid within the field boundary.

        Parameters
        ----------
        numdivs : array_like of int, length 2
            [Number of columns, number of ranges]
        field_layer : str, optional
            Name of layer with field boundary. Defaults to None.
        """
        _napari_grid(self.viewer, numdivs, layername=self.layer_dict["field_boundary"])
        self.layer_dict["grid_lines_columns"] = "grid_lines1"
        self.layer_dict["grid_lines_ranges"] = "grid_lines2"

    def plots(self, plot_layer="Plots"):
        """Add layer with polygons defined by gridded lines.

        Parameters
        ----------
        plot_layer : str, optional
            Name of new layer created. Defaults to "Plots".
        """
        _napari_polygon_grid(self.viewer, plot_layer,
                             lines1=self.layer_dict["grid_lines_columns"],
                             lines2=self.layer_dict["grid_lines_ranges"])
        self.layer_dict["plot_polygons"] = plot_layer

    def to_points(self, dest=None, layername="Points"):
        """Make an array of coordinates or save a geojson of points from an InteractiveShapes object

        Parameters:
        -----------
        dest : str, Optional
            Path to save a geojson file to if desired. Defaults to None, which will return the points as an array instead of writing a geojson shapefile.
        layername : str, Optional
            Name of the viewer layer from which to take the points. Defaults to "Points"

        Returns:
        --------
        list or dict, if dest is None then a list of coordinates, if dest is str then a dictionary of what was written to the geojson file.
        """
        if dest is None:
            # if dest is None then we want to return the points as if we read them from a geojson file
            # NOTE we could have a flag in points/shapes that looks for if dest is None in addition to what source is,
            # NOTE then if dest is None it doesn't write the geojson, it just returns the data. I actually rather like that.
            return _viewer_to_points(img=self.img, viewer=self.viewer, layername=layername)
        # otherwise we are writing a geojson
        return points(img=self.img, source=self.viewer, dest=dest, layername=layername)

    def to_shape(self, dest=None, shapetype="polygon", layername="Shapes"):
        """Make a polygon array or save a geojson of polygons from an InteractiveShapes object

        Parameters:
        -----------
        dest : str, optional
            Path to save to a geojson file to save if source is a Napari viewer or Points object.
            Defaults to None, only required if 'source' is a Napari view or Points object.
        shapetype: str, optional
            Geometry type from Napari viewer shape layer desired for geojson output, defaults to "polygon."
        layername: str, optional
            Name of shapes layer, defaults to "Shapes."

        Returns:
        --------
        list or dict, if dest is a str then a geojson is written and a dictionary is returned
            If dest is None (the default) then returns a list of X,Y coordinates.
        """
        if dest is None:
            # possibly another custom viewer_to_polygon function like _viewer_to_points below
            return 1
        return shapes(img=self.img, source=self.viewer, dest=dest, shapetype=shapetype, layername=layername)


def _viewer_to_points(img, viewer, layername="Points"):
    """Return points from a viewer as though using convert.points on a geojson file

    Parameters:
    -----------
    img : plantcv.plantcv.classes.Spectral_data
        The image used for clicking on points, should be from read_geotif.
    viewer: Napari.viewer or plantcv.annotate.classes.Points object.
        The viewer used to make the clicks.
    layername : str
        Name of the Napari viewer layer from which to take points.

    Returns:
    --------
    pts_return : ???, transformed points from the viewer
    """
    # Napari output, points must be reversed
    if hasattr(viewer, 'layers'):
        pts = [(img.metadata["transform"]*reversed(i)) for i in viewer.layers[layername].data]
        pts_return = [reversed(i) for i in viewer.layers[layername].data]
    # Annotate output
    elif hasattr(viewer, 'coords'):
        pts = [(img.metadata["transform"]*i) for i in viewer.coords['default']]
        pts_return = viewer.coords['default']
    else:
        fatal_error("Viewer class type not recognized. Currently, Napari and PlantCV-annotate viewers supported.")
    return pts_return
