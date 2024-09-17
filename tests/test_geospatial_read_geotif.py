"""Tests for geospatial.read_geotif."""

import pytest
from plantcv.geospatial import read_geotif


def test_geospatial_read_geotif(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = read_geotif(filename=test_data.cropped_tif, bands="B,G,R,RE,N")
    assert img.array_data.shape[2] == 5


def test_geospatial_read_geotif_rgb(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    assert img.pseudo_rgb.shape == (284, 261, 3)


def test_geospatial_read_geotif_bad_input(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    with pytest.raises(RuntimeError):
        _ = read_geotif(filename=test_data.cropped_tif, bands="p")


def test_geospatial_read_geotif_bad_crop(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    with pytest.raises(RuntimeError):
        _ = read_geotif(filename=test_data.empty_tif, bands="B,G,R,RE,N")


def test_geospatial_read_geotif_polygon_crop(test_data):
    """Test for plantcv-geospatial."""
    # read in rgb image with a polygon-type shapefile
    img = read_geotif(filename=test_data.rgb_tif, bands=[650, 560, 480],
                      cropto=test_data.square_crop)
    assert img.pseudo_rgb.shape == (80, 83, 3)


def test_geospatial_read_geotif_point_crop(test_data):
    """Test for plantcv-geospatial."""
    # read in rgb image with a polygon-type shapefile
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B", cropto=test_data.point_crop)
    assert img.pseudo_rgb.shape == (41, 46, 3)
