"""Tests for geospatial.convert.to_roi"""

import joblib
import pytest
import numpy as np
from plantcv.geospatial.convert.to_roi import to_roi


def test_geospatial_points_to_roi(test_data):
    """Test for plantcv-geospatial."""
    # read in small 3-band tif image
    img = joblib.load(test_data.rgb_pickled)
    rois = to_roi(img=img, geojson=test_data.pts_geojson, radius=0.5)
    assert np.all(rois.contours[0][0][0] == np.array([119, 170]))


def test_geospatial_polygon_to_roi(test_data):
    """Test for plantcv-geospatial."""
    # read in small 3-band tif image
    img = joblib.load(test_data.rgb_pickled)
    roi = to_roi(img=img, geojson=test_data.square_crop)
    assert np.all(roi.contours == np.array([[196, 115], [145, 78], [114, 120], [165, 157]]))


def test_geospatial_points_to_roi_badinput(test_data):
    """Test for plantcv-geospatial."""
    img = joblib.load(test_data.rgb_pickled)
    with pytest.raises(RuntimeError):
        _ = to_roi(img=img, geojson=test_data.square_crop, radius=0.5)


def test_geospatial_polygon_to_roi_badinput(test_data):
    """Test for plantcv-geospatial."""
    img = joblib.load(test_data.rgb_pickled)
    with pytest.raises(RuntimeError):
        _ = to_roi(img=img, geojson=test_data.pts_geojson)
