"""Tests for geospatial.analyze.spectral"""

import dill as pickle
import pytest
from plantcv.plantcv import outputs, params
from plantcv.geospatial.analyze import spectral_index as analyze_spectral


@pytest.mark.parametrize("debug,percentiles", [["print", None],
                                               ["plot", None],
                                               [None, [33, 75, 92]]])
def test_analyze_spectral_index(debug, tmpdir, test_data, percentiles):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    # Read in test data
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    #img.nodata = 0
    # Change wavelengths so it will try to calculate index
    img.wavelengths = [700, 530, 460]
    # Debug mode
    params.debug = debug
    _ = analyze_spectral(img=img, index="egi", geojson=test_data.poly_crop_fid, percentiles=percentiles)
    assert outputs.observations["default_888"]['percentile_75_index_egi']["value"] <= 1
