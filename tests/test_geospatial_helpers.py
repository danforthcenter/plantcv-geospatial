"""Tests for geospatial._helpers"""

from plantcv.geospatial._helpers import _transform_geojson_crs
from plantcv.geospatial import read_geotif

def test_geospatial_helpers_transform_geojson_crs(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = read_geotif(filename=test_data.rgb_tif, bands="B,G,R")
    gdf = _transform_geojson_crs(img=img, geojson=test_data.epsg4326_geojson)
    assert gdf.crs == img.metadata['crs']
