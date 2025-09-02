"""Tests for geospatial.analyze.spectral"""

import joblib
import pytest
from plantcv.plantcv import outputs, params
from plantcv.geospatial.analyze import spectral_index as analyze_spectral


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_analyze_spectral_index(debug, tmpdir, test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    # Read in test data
    img = joblib.load(test_data.multi_pickled)
    img.metadata['nodata'] = 0
    img.array_data = img.array_data[:, :, 2]  # Make a grayscale img to use as index
    # Debug mode
    params.debug = debug
    _ = analyze_spectral(img=img, geojson=test_data.multipolygon)
    assert outputs.observations["default_1"]["percentile_75_datacube"]["value"] <= 1
