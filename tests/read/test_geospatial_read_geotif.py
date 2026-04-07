"""Tests for geospatial.read.geotif."""

import pytest
from plantcv.geospatial.read import geotif
from plantcv.geospatial.images import GEO, DSM


def test_geospatial_read_geotif(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = geotif(filename=test_data.cropped_tif, bands="B,G,R,RE,N")
    assert img.shape[2] == 5
    assert isinstance(img, GEO)


def test_geospatial_read_geotif_rgb(test_data):
    """Test for plantcv-geospatial."""
    # read in small tif image
    img = geotif(filename=test_data.rgb_tif, bands="R,G,B")
    assert img.thumb.shape == (284, 261, 3)


def test_geospatial_read_geotif_rgb_uint16(test_data):
    """Test for plantcv-geospatial."""
    # read in small tif image
    img = geotif(filename=test_data.rgb_uint16_tif, bands="R,G,B")
    assert img.thumb.shape == (284, 261, 3)
    

def test_geospatial_read_geotif_bad_input(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    with pytest.raises(RuntimeError):
        _ = geotif(filename=test_data.cropped_tif, bands="p")


def test_geospatial_read_geotif_too_few_bands(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = geotif(filename=test_data.rgb_tif, bands="R,G")
    # this should work still but would issue a warning
    assert img.thumb.shape == (284, 261, 3)


def test_geospatial_read_geotif_bad_crop(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    with pytest.raises(RuntimeError):
        _ = geotif(filename=test_data.empty_tif, bands="B,G,R,RE,N")

        
def test_geospatial_read_geotif_bad_bands(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    with pytest.raises(RuntimeError):
        _ = geotif(filename=test_data.rgb_tif, bands="B,G,R,RE,N")


def test_geospatial_read_geotif_polygon_crop(test_data):
    """Test for plantcv-geospatial."""
    # read in rgb image with a polygon-type shapefile
    img = geotif(filename=test_data.rgb_tif, bands=[650, 560, 480],
                      cropto=test_data.square_crop)
    assert img.thumb.shape == (80, 83, 3)


def test_geospatial_read_geotif_point_crop(test_data):
    """Test for plantcv-geospatial."""
    # read in rgb image with a polygon-type shapefile
    img = geotif(filename=test_data.rgb_tif, bands="R,G,B", cropto=test_data.point_crop)
    assert img.thumb.shape == (41, 46, 3)


def test_geospatial_read_geotif_gray(test_data):
    """Test for plantcv-geospatial."""
    # read in small gray image
    img = geotif(filename=test_data.gray_tif, bands="gray", cutoff=0.99)
    assert img.shape[0] == 411
    assert isinstance(img, DSM)
