"""Tests for geospatial.center_grid_rois"""

import napari
import dill as pickle
import pytest
import numpy as np
from plantcv.geospatial.center_grid_rois import center_grid_rois
from plantcv.geospatial.create_shapes.interactive_shapes import InteractiveShapes


def test_geospatial_center_rois_none(test_data):
    """Test for plantcv-geospatial."""
    field = np.array([])
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, show=False)
    editor.add_layer()
    with pytest.raises(RuntimeError):
        center_grid_rois(editor, radius=10)
    editor.viewer.close()


def test_geospatial_center_rois_one(test_data):
    """Test for plantcv-geospatial."""
    field = np.array([[64.11229125, 128.74165877],
                      [136.25692447, 203.82241079],
                      [213.85434974, 139.64724287],
                      [140.45137989,  59.95258989]])
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, show=False)
    editor.viewer.add_shapes(field, name="Shapes")
    rois = center_grid_rois(editor, radius=10)
    assert len(rois.contours) == 1
    editor.viewer.close()


def test_geospatial_center_rois_multi(test_data):
    """Test for plantcv-geospatial."""
    field = [np.array([[33.91221223, 186.62514357],
                       [71.24286547, 238.63639077],
                       [111.92908304, 196.27239103],
                       [73.34009318, 151.81116358]]), 
             np.array([[98.08738015, 122.86942119],
                       [143.80694423, 174.88066839],
                       [187.00983506, 135.0333419],
                       [143.80694423,  83.44154024]])]
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    editor = InteractiveShapes(img, show=False)
    editor.viewer.add_shapes(field, name="Shapes")
    rois = center_grid_rois(editor, radius=10)
    assert len(rois.contours) == 2
    editor.viewer.close()
