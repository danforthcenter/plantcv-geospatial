import pytest
import joblib
from plantcv.plantcv import outputs, params
from plantcv.geospatial.analyze import height_percentile


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_height_percentile(debug, tmpdir, test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    # Debug mode
    params.debug = debug
    _ = height_percentile(dsm=img, geojson=test_data.square_crop)
    assert outputs.observations["default_0"]["plant_height"]["value"] > 0


def test_height_percentile_with_geo_ids(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    _ = height_percentile(dsm=img, geojson=test_data.geojson_with_id)
    assert outputs.observations["888"]["plant_height"]["value"] > 0
