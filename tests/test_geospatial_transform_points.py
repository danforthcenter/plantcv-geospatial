"""Tests for geospatial.transform_points"""

from plantcv.geospatial import read_geotif, transform_points


def test_geospatial_transform_points(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = read_geotif(filename=test_data.rgb_tif, bands="B,G,R")
    coords = transform_points(img=img, geojson=test_data.pts_geojson)
    assert len(coords) == 4


def test_geospatial_transform_single_points(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = read_geotif(filename=test_data.rgb_tif, bands="B,G,R")
    coords = transform_points(img=img, geojson=test_data.single_pts_geojson)
    assert len(coords) == 8
