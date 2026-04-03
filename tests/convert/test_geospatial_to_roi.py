"""Tests for geospatial.convert.to_roi"""

import dill as pickle
import pytest
import numpy as np
from plantcv.geospatial.convert.to_roi import to_roi


def test_geospatial_points_to_roi(test_data):
    """Test for plantcv-geospatial."""
    # read in small 3-band tif image
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    rois = to_roi(img=img, geojson=test_data.single_points, radius=0.5)
    assert np.all(rois.contours[0][0][0] == np.array([1801, 496]))


def test_geospatial_polygon_to_roi(test_data):
    """Test for plantcv-geospatial."""
    # read in small 3-band tif image
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    roi = to_roi(img=img, geojson=test_data.poly_crop)
    assert np.all(roi.contours == np.array([[1551, 764], [2484, 1547],
                                            [1640, 2525], [706, 1681]]))


def test_geospatial_points_to_roi_badinput(test_data):
    """Test for plantcv-geospatial."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    with pytest.raises(RuntimeError):
        _ = to_roi(img=img, geojson=test_data.poly_crop, radius=0.5)


def test_geospatial_polygon_to_roi_badinput(test_data):
    """Test for plantcv-geospatial."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    with pytest.raises(RuntimeError):
        _ = to_roi(img=img, geojson=test_data.single_points)
