"""Tests for geospatial.transform_polygons"""

import joblib
from plantcv.geospatial import transform_polygons


def test_geospatial_transform_polygons(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = joblib.load(test_data.rgb_pickled)
    coords = transform_polygons(img=img, geojson=test_data.square_crop)
    assert coords == [[[196, 115], [145, 78], [114, 120], [165, 157]]]


def test_geospatial_transform_single_polygons(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = joblib.load(test_data.rgb_pickled)
    coords = transform_polygons(img=img, geojson=test_data.multipolygon)
    assert coords[0] == [[167, 28], [200, 52], [176, 85], [143, 60]]
