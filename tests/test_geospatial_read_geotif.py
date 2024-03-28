"""Tests for geospatial.readd_geotif."""

import cv2
import pytest
from plantcv.geospatial import read_geotif


def test_geospatial_read_geotif(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image 
    img = read_geotif(filename=test_data.cropped_tif, bands="B,G,R,RE,N")
    assert img.array_data.shape[2] == 5


def test_geospatial_read_geotif_bad_input(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image 
    with pytest.raises(RuntimeError):
        img = read_geotif(filename=test_data.cropped_tif, bands="p")
