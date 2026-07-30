"""Tests for geospatial.analyze.chm"""

import dill as pickle
from plantcv.plantcv import outputs
from plantcv.geospatial.analyze import chm


def test_analyze_chm(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    with open(test_data.dsm_pickled, "rb") as f:
        img = pickle.load(f)
    img.nodata = 0
    _ = chm(dsm=img, geojson=test_data.poly_crop)
    assert outputs.observations["default_888"]["height_mean"]["value"] > 0