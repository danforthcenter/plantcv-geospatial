# PlantCV-Geospatial classes

import napari
from plantcv.plantcv import fatal_error
from plantcv.geospatial.create_shapes.napari_grid import _napari_grid
from plantcv.geospatial.create_shapes.napari_polygon_grid import _napari_polygon_grid


class InteractiveShapes:
    """Plantcv-Geospatial interactive shapes class."""

    def __init__(self, img, viewer_type="napari", field_layer=None, show=True):
        """Initialize parameters.

        Parameters
        ----------
        viewer : str
            Type of viewer to initialize. Defaults to "napari".
        img : plantcv.plantcv.classes.Spectral_data
            Image to add to the first layer in an initialized viewer. Defaults to None.
        field_layer : str, optional
            Name to call the first added shapes layer. Defaults to None.
        """
        self.device = 0
        if viewer_type == "napari":
            self.viewer = napari.Viewer(show=show)
        else:
            fatal_error("Only napari viewers are currently supported.")

        self.img = img
        self.layer_dict = {}
        self.viewer.add_image(img.pseudo_rgb)
        if field_layer is not None:
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
