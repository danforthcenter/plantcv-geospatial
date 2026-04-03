"""Tests for geospatial.analyze.height_subtraction"""

import dill as pickle
import pytest
import numpy as np
from plantcv.plantcv import outputs, params
from plantcv.geospatial.analyze import height_subtraction


def test_height_subtraction(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = "plot"
    # Read in test data
    with open(test_data.dsm_pickled, "rb") as f:
        dsm = pickle.load(f)
    dsm.nodata = None
    test = height_subtraction(dsm1=dsm, dsm0=dsm)
    assert np.nansum(test) == 0

#def test_height_subtraction_metadata(test_data):
#    """Test for PlantCV."""
#    # Clear previous outputs
#    outputs.clear()
#    # Debug mode
#    params.debug = "plot"
#    # Read in test data
#    dsm = joblib.load(test_data.rgb_pickled)
#    # Setting metadata
#    dsm.metadata['nodata'] = 1
#    test = height_subtraction(dsm1=dsm, dsm0=dsm)
#    assert np.sum(test.array_data) == 0

def test_height_subtraction_unequal_crs(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = "plot"
    # Read in test data
    with open(test_data.dsm_pickled, "rb") as f:
        dsm1 = pickle.load(f)
    dsm1.nodata = None
    with open(test_data.dsm_pickled, "rb") as f:
        dsm0 = pickle.load(f)
    dsm0.nodata = None
    # Overwriting CRS
    dsm1.crs = 0
    with pytest.raises(RuntimeError):
        _ = height_subtraction(dsm1, dsm0)

def test_height_shape_check(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Debug mode
    params.debug = "plot"
    # Read in test data
    with open(test_data.dsm_pickled, "rb") as f:
        dsm1 = pickle.load(f)
    dsm1.nodata = None
    with open(test_data.geo_pickled, "rb") as f:
        dsm0 = pickle.load(f)
    # Check for shape
    with pytest.raises(RuntimeError):
        _ = height_subtraction(dsm1, dsm0)      
