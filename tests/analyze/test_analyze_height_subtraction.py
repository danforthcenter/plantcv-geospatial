"""Tests for geospatial.analyze.height_subtraction"""

import joblib
import pytest
import numpy as np
from plantcv.plantcv import outputs, params
from plantcv.plantcv import fatal_error
from plantcv.geospatial.analyze import height_subtraction


def test_height_subtraction(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = "plot"
    # Read in test data
    dsm = joblib.load(test_data.rgb_pickled)
    test = height_subtraction(dsm1=dsm, dsm0=dsm)
    assert np.sum(test.array_data) == 0

def test_height_subtraction_metadata(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = "plot"
    # Read in test data
    dsm = joblib.load(test_data.rgb_pickled)
    # Setting metadata
    dsm.metadata['nodata'] = 1
    test = height_subtraction(dsm1=dsm, dsm0=dsm)
    assert np.sum(test.array_data) == 0

def test_height_subtraction_unequal_crs(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = "plot"
    # Read in test data
    dsm1_fake = joblib.load(test_data.rgb_pickled)
    dsm0_fake = joblib.load(test_data.rgb_pickled)
    # Overwriting CRS
    dsm1_fake.metadata["crs"] = 0
    with pytest.raises(RuntimeError):
        test = height_subtraction(dsm1=dsm1_fake, dsm0=dsm0_fake)

def test_height_shape_check(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = "plot"
    # Read in test data
    dsm1_fake = joblib.load(test_data.rgb_pickled)
    dsm0_fake = joblib.load(test_data.multi_pickled)
    # Check for shape
    with pytest.raises(ValueError):
       test = height_subtraction(dsm1=dsm1_fake, dsm0=dsm0_fake)      
