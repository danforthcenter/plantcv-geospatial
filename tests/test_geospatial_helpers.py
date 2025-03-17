"""Tests for geospatial._helpers"""

import joblib
from plantcv.geospatial._helpers import _transform_geojson_crs

def test_geospatial_helpers_transform_geojson_crs(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = joblib.load(test_data.rgb_pickled)
    gdf = _transform_geojson_crs(img=img, geojson=test_data.epsg4326_geojson)
    assert gdf.crs == img.metadata['crs']
