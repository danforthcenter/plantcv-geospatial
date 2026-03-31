"""Tests for geospatial.transform_polygons"""

import dill as pickle
from plantcv.geospatial import transform_polygons


def test_geospatial_transform_polygons(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    coords = transform_polygons(img=img, geojson=test_data.poly_crop)
    assert coords == [[[1551, 764], [2484, 1547], [1640, 2525], [706, 1681]]]


def test_geospatial_transform_single_polygons(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    coords = transform_polygons(img=img, geojson=test_data.multipolygon)
    assert coords[0] == [[1601, 350], [1931, 350], [1931, 652], [1601, 652]]
