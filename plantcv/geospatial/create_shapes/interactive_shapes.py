# PlantCV-Geospatial classes

import napari
from plantcv.plantcv import fatal_error
from plantcv.geospatial.create_shapes.napari_grid import _napari_grid
from plantcv.geospatial.create_shapes.napari_polygon_grid import _napari_polygon_grid
from plantcv.geospatial.convert.points import points
from plantcv.geospatial.convert.shapes import shapes
from plantcv.geospatial import field_layout


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
        self.viewer.add_image(img.thumb)
        self.viewer.add_shapes(name=field_layer)
        self.layer_dict["field_boundary"] = field_layer

    def add_layer(self, layer_type="shapes", layername="Shapes"):
        """Add a layer to the viewer.

        Parameters
        ----------
        layer_type : str, optional
            Type of layer to add. Options are "shapes" or "points". Defaults to "shapes".
        layername : str, optional
            Name of added layer. Defaults to "Shapes".
        """
        if layer_type == "shapes":
            self.viewer.add_shapes(name=layername)
            self.layer_dict["shapes_"+str(self.device)] = layername
            self.device += 1
        elif layer_type == "points":
            self.viewer.add_points(name=layername)
            self.layer_dict["points_"+str(self.device)] = layername
            self.device += 1
        else:
            fatal_error(f"Layer type {layer_type} is not supported. Layer_type must be 'shapes' or 'points'.")

    def grid(self, numdivs=None):
        """Add layers with lines forming a grid within the field boundary.

        Parameters
        ----------
        numdivs : array_like of int, length 2; Defaults to None.
            [Number of columns, number of ranges]
        field_layer : str, optional
            Name of layer with field boundary. Defaults to None.
        """
        if numdivs is None:
            if field_layout is None:
                fatal_error("FieldLayout is not available on img; cannot determine numdivs.")
            num_columns = getattr(field_layout, "num_columns", None)
            num_ranges = getattr(field_layout, "num_ranges", None)
            if num_columns is None or num_ranges is None:
                    fatal_error("num_columns and num_ranges are not available on FieldLayout;cannot determine numdivs.")
            numdivs = [num_columns, num_ranges]

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
            Path to save a geojson file to save points if desired.
            Defaults to None, which will return the points
            as an array instead of writing a geojson shapefile.
        layername : str, Optional
            Name of the viewer layer from which to take the points. Defaults to "Points"

        Returns:
        --------
        list
            List of point coordinates from viewer layer
        """
        return points(img=self.img, source=self.viewer, dest=dest, layername=layername)

    def to_shapes(self, dest=None, shapetype="polygon", layername="Shapes"):
        """Make a polygon array or save a geojson of polygons from an InteractiveShapes object

        Parameters:
        -----------
        dest : str, optional
            Path to save to a geojson file to save shapes if desired.
            Defaults to None which will return shapes as an array
            instead of writing to a geojson shapefile.
        shapetype: str, optional
            Geometry type from Napari viewer shape layer desired for geojson output, defaults to "polygon."
        layername: str, optional
            Name of shapes layer, defaults to "Shapes."

        Returns:
        --------
        list
            List of X,Y coordinates of shape vertices.
        """
        return shapes(img=self.img, source=self.viewer, dest=dest, shapetype=shapetype, layername=layername)
