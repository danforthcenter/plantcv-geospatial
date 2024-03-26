"""Tests for geospatial.readd_geotif."""

import cv2
import geospatial.read_geotif 


def test_geospatial_read_geotif(test_data):
    """Test for plantcv-geospatial."""
    img = read_geotif(filename=test_data.cropped_tif, bands="B,G,R,RE,N")
    assert img.array_data.shape[2] == 978
