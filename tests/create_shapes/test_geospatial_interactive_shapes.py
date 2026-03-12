"""Tests for geospatial.classes.InteractiveShapes"""

import pytest
import joblib
import numpy as np
from plantcv.geospatial import InteractiveShapes
from plantcv.geospatial.create_shapes.napari_polygon_grid import _lineintersect


def test_geospatial_interactive_grid(test_data):
    """Test for plantcv-geospatial."""
    field = np.array([[64.11229125, 128.74165877],
                      [136.25692447, 203.82241079],
                      [213.85434974, 139.64724287],
                      [140.45137989,  59.95258989]])
    img = joblib.load(test_data.rgb_pickled)
    editor = InteractiveShapes(img, field_layer="dummy_layer", show=False)
    editor.viewer.add_shapes(field, name="field_bounds")
    editor.layer_dict["field_boundary"] = "field_bounds"
    editor.grid(numdivs=[1,2])
    editor.plots()
    assert len(editor.viewer.layers["grid_lines1"].data) == 2
    assert len(editor.viewer.layers["Shapes"].data) == 2
    assert int(editor.viewer.layers["grid_lines1"].data[0][1][0]) == 140
    assert int(editor.viewer.layers["Shapes"].data[0][1][0]) == 136
    editor.viewer.close()


def test_interactive_addshapes(test_data):
    """Test for plantcv-geospatial."""
    img = joblib.load(test_data.rgb_pickled)
    editor = InteractiveShapes(img, show=False)
    editor.add_layer()
    assert editor.device == 1


def test_interactive_addpoints(test_data):
    """Test for plantcv-geospatial."""
    img = joblib.load(test_data.rgb_pickled)
    editor = InteractiveShapes(img, show=False)
    editor.add_layer(layer_type="points", layer_name="Points")
    assert editor.device == 1


def test_interactive_wronglayername(test_data):
    """Test for plantcv-geospatial."""
    img = joblib.load(test_data.rgb_pickled)
    editor = InteractiveShapes(img, show=False)
    with pytest.raises(RuntimeError):
        editor.add_layer(layer_type="nonsense")


def test_geospatial_lineintersect():
    """Test for plantcv-geospatial."""
    with pytest.raises(RuntimeError):
        _ = _lineintersect([(0, 0), (0, 1)], [(1, 0), (1, 1)])
