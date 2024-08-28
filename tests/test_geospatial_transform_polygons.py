"""Tests for geospatial.transform_polygons"""

from plantcv.geospatial import read_geotif, transform_polygons


def test_geospatial_transform_points(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = read_geotif(filename=test_data.rgb_tif, bands="B,G,R")
    coords = transform_polygons(img=img, geojson=test_data.square_crop)
    assert coords == [[[196, 115], [145, 78], [114, 120], [165, 157]]]


def test_geospatial_transform_single_points(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = read_geotif(filename=test_data.rgb_tif, bands="B,G,R")
    coords = transform_polygons(img=img, geojson=test_data.multipolygon)
    assert coords[0] == [[167, 28], [200, 52], [176, 85], [143, 60]]
