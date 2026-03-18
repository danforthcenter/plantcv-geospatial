# PlantCV-Geospatial classes

import napari
from plantcv.plantcv import fatal_error
from plantcv.geospatial.create_shapes.napari_grid import _napari_grid
from plantcv.geospatial.create_shapes.napari_polygon_grid import _napari_polygon_grid


class Field_layout:
    """PlantCV-Geospatial field layout metadata class."""

    def __init__(self, num_ranges=None, num_columns=None, range_length=None,
                 row_length=None, num_rows=1, range_spacing=0, column_spacing=0):
        """Initialize parameters.

        Parameters
        ----------
        num_ranges : int
            Number of ranges in the field layout.
        num_columns : int
            Number of columns in the field layout.
        range_length : float
            Length of each range in units that should match input shapefiles.
        row_length : float
            Length of each row in a plot.
        num_rows: int, optional
            Number of rows in a plot. Defaults to 1.
        range_spacing : float, optional
            Length of alleys between ranges. Defaults to 0.
        column_spacing : float, optional
            Lenght of alleys between columns. Defaults to 0.
        """
        self.num_ranges = num_ranges
        self.num_columns = num_columns
        self.range_length = range_length
        self.row_length = row_length
        self.num_rows = num_rows
        self.range_spacing = range_spacing
        self.column_spacing = column_spacing


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
