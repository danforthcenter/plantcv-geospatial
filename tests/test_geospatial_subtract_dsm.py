"""Tests for geospatial.subtract_dsm"""

import dill as pickle
import pytest
import numpy as np
from plantcv.geospatial import subtract_dsm
from plantcv.plantcv import outputs


def test_subtract_dsm(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    with open(test_data.dsm_pickled, "rb") as f:
        dsm = pickle.load(f)
    dsm.nodata = None
    test = subtract_dsm(dsm1=dsm, dsm0=dsm)
    assert np.nansum(test) == 0

def test_subtract_dsm_unequal_crs(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
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
        _ = subtract_dsm(dsm1, dsm0)

def test_subtract_dsm_shape_check(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    with open(test_data.dsm_pickled, "rb") as f:
        dsm1 = pickle.load(f)
    dsm1.nodata = None
    with open(test_data.geo_pickled, "rb") as f:
        dsm0 = pickle.load(f)
    # Check for shape
    with pytest.raises(RuntimeError):
        _ = subtract_dsm(dsm1, dsm0)      
