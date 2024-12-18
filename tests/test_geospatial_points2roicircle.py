"""Tests for geospatial.points2roi_circle"""

from plantcv.geospatial import read_geotif, points2roi_circle
import numpy as np


def test_geospatial_points2roi_circle(test_data):
    """Test for plantcv-geospatial."""
    # read in small 3-band tif image
    img = read_geotif(filename=test_data.rgb_tif, bands="B,G,R")
    rois = points2roi_circle(img=img, geojson=test_data.pts_geojson, radius=0.5)
    assert np.all(rois.contours[0][0][0] == np.array([119, 170]))
