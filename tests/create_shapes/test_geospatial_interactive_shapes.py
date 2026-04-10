"""Tests for geospatial.classes.InteractiveShapes"""

import pytest
import dill as pickle
import numpy as np
from plantcv.geospatial.create_shapes.interactive_shapes import InteractiveShapes
from plantcv.geospatial.create_shapes.napari_polygon_grid import _lineintersect
from plantcv.geospatial import field_layout


def test_geospatial_interactive_grid(test_data):
    """Test for plantcv-geospatial."""
    field = np.array([[64.11229125, 128.74165877],
                      [136.25692447, 203.82241079],
                      [213.85434974, 139.64724287],
                      [140.45137989,  59.95258989]])
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, field_layer="dummy_layer", show=False)
    editor.viewer.add_shapes(field, name="field_bounds")
    editor.layer_dict["field_boundary"] = "field_bounds"
    editor.grid(numdivs=[1,2])
    editor.plots()
    assert len(editor.viewer.layers["grid_lines1"].data) == 2
    assert len(editor.viewer.layers["Plots"].data) == 2
    assert int(editor.viewer.layers["grid_lines1"].data[0][1][0]) == 140
    assert int(editor.viewer.layers["Plots"].data[0][1][0]) == 136
    editor.viewer.close()

def test_geospatial_interactive_grid_empty_numdivs(test_data):
    """Test for plantcv.geospatial."""
    field = np.array([[64.11229125, 128.74165877],
                      [136.25692447, 203.82241079],
                      [213.85434974, 139.64724287],
                      [140.45137989,  59.95258989]])
    field_layout.num_columns = 1
    field_layout.num_ranges = 2
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, field_layer="dummy_layer", show=False)
    editor.viewer.add_shapes(field, name="field_bounds")
    editor.layer_dict["field_boundary"] = "field_bounds"
    editor.grid()
    editor.plots()
    assert len(editor.viewer.layers["grid_lines1"].data) == 2
    assert len(editor.viewer.layers["Plots"].data) == 2
    editor.viewer.close()

def test_geospatial_interactive_badviewer(test_data):
    """Test for plantcv-geospatial."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    with pytest.raises(RuntimeError):
        _ = InteractiveShapes(img, viewer_type="nonsense", show=False)


def test_geospatial_interactive_addshapes(test_data):
    """Test for plantcv-geospatial."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, show=False)
    editor.add_layer()
    assert editor.device == 1
    editor.viewer.close()


def test_geospatial_interactive_addpoints(test_data):
    """Test for plantcv-geospatial."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, show=False)
    editor.add_layer(layer_type="points", layername="Points")
    assert editor.device == 1
    editor.viewer.close()


def test_geospatial_interactive_wronglayername(test_data):
    """Test for plantcv-geospatial."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, show=False)
    with pytest.raises(RuntimeError):
        editor.add_layer(layer_type="nonsense")


def test_geospatial_lineintersect():
    """Test for plantcv-geospatial."""
    with pytest.raises(RuntimeError):
        _ = _lineintersect([(0, 0), (0, 1)], [(1, 0), (1, 1)])


def test_geospatial_interactive_to_shapes(test_data):
    """Test for plantcv-geospatial."""
    field = np.array([[64.11229125, 128.74165877],
                      [136.25692447, 203.82241079],
                      [213.85434974, 139.64724287],
                      [140.45137989,  59.95258989]])
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, field_layer="dummy_layer", show=False)
    editor.viewer.add_shapes(field, name="field_bounds")
    editor.layer_dict["field_boundary"] = "field_bounds"
    # instead of calling the add_layer method we make a layer manually to test
    editor.viewer.add_shapes(field, shape_type="polygon", name="Shapes")
    x = editor.to_shapes()
    assert len(x[0]) == 4



def test_geospatial_interactive_to_points(test_data):
    """Test for plantcv-geospatial."""
    field = np.array([[64.11229125, 128.74165877],
                      [136.25692447, 203.82241079],
                      [213.85434974, 139.64724287],
                      [140.45137989,  59.95258989]])
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, field_layer="dummy_layer", show=False)
    editor.viewer.add_shapes(field, name="field_bounds")
    editor.layer_dict["field_boundary"] = "field_bounds"
    # instead of calling the add_layer method we make a layer manually to test
    editor.viewer.add_points(field, name="Points")
    x = editor.to_points()
    assert len(x) == 4
