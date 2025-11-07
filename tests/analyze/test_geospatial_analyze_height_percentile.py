"""Tests for geospatial.analyze.height_percentile"""

import joblib
from plantcv.plantcv import outputs, params
from plantcv.geospatial.analyze import height_percentile


def test_height_percentile(tmpdir, test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    img.metadata['nodata'] = 0
    # Debug mode
    params.debug = "print"
    _ = height_percentile(dsm=img, geojson=test_data.square_crop)
    assert outputs.observations["default_0"]["plant_height"]["value"] > 0


def test_height_percentile_with_geo_ids(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = None
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    _ = height_percentile(dsm=img, geojson=test_data.geojson_with_id, label="test")
    assert outputs.observations["test_888"]["plant_height"]["value"] > 0
    
def test_height_percentile_with_geo_fids(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = "plot"
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    _ = height_percentile(dsm=img, geojson=test_data.square_crop_with_plotname, label="test")
    assert outputs.observations["test_888"]["plant_height"]["value"] > 0
