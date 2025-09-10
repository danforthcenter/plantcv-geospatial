"""Tests for geospatial.analyze.height_subtraction"""

import joblib
from plantcv.plantcv import outputs, params
from plantcv.geospatial.analyze import height_subtraction


def test_height_subtraction(testdata):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = "plot"
    # Read in test data
    dsm = joblib.load(test_data.rgb_pickled)
    test = height_subtraction(dsm1=dsm, dsm0=dsm)
    assert sum(test.arraydata) == 0
