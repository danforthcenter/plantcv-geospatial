"""Tests for geospatial.analyze.spectral"""

import dill as pickle
import pytest
from plantcv.plantcv import outputs, params
from plantcv.geospatial.analyze import spectral_index as analyze_spectral
import numpy as np


@pytest.mark.parametrize("debug,percentiles,index", [["print", None, "evi"],
                                               ["plot", None, "evi"],
                                               [None, [33, 75, 92], "egi"]])
def test_analyze_spectral_index(debug, tmpdir, test_data, percentiles, index):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    # Read in test data
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    # Set nodata since pickled doesn't have it
    img.nodata = 0
    # Change wavelengths so it will try to calculate index
    img.wavelengths = [700, 530, 460]
    # Create mask 
    mask = np.ones(shape=(img.shape[0],img.shape[1]))
    # Debug mode
    params.debug = debug
    _ = analyze_spectral(img=img, index=index, geojson=test_data.poly_crop_fid,
                         mask=mask, percentiles=percentiles, distance=100)
    assert outputs.observations["default_888"]['percentile_75_index_' + index]["value"] <= 1
