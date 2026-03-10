"""Tests for geospatial.convert.points_to_roi_circle"""

import numpy as np
import joblib
from plantcv.geospatial.convert.to_roi import to_roi


def test_geospatial_points_to_roi(test_data):
    """Test for plantcv-geospatial."""
    # read in small 3-band tif image
    img = joblib.load(test_data.rgb_pickled)
    rois = to_roi(img=img, geojson=test_data.pts_geojson, radius=0.5)
    assert np.all(rois.contours[0][0][0] == np.array([119, 170]))
