"""Tests for geospatial.points2roi_circle"""

import numpy as np
import joblib
from plantcv.geospatial import points2roi_circle


def test_geospatial_points2roi_circle(test_data):
    """Test for plantcv-geospatial."""
    # read in small 3-band tif image
    img = joblib.load(test_data.rgb_pickled)
    rois = points2roi_circle(img=img, geojson=test_data.pts_geojson, radius=0.5)
    assert np.all(rois.contours[0][0][0] == np.array([119, 170]))
