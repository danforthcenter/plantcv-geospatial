"""Tests for geospatial.write_geotif"""

import dill as pickle
import os
import numpy as np
import pytest
from plantcv.geospatial.write_geotif import write_geotif

def test_write_geotif(test_data, tmpdir):
    """Test write_geotif with a DSM."""
    cache_dir = tmpdir.mkdir("cache")
    with open(test_data.dsm_pickled, "rb") as f:
        img = pickle.load(f)
    filename = os.path.join(cache_dir, 'outputs/test_out.geotif')
    img.nodata = 0
    write_geotif(filename, img)
    assert os.path.exists(filename)
    
def test_write_geotif_array(test_data, tmpdir):
    """Test write_geotif with an RGB array."""
    cache_dir = tmpdir.mkdir("cache")
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    filename = os.path.join(cache_dir, 'test_out.geotif')
    img.nodata = 0
    # Test 2D array
    img.thumb = np.squeeze(img.thumb, axis=-1)
    write_geotif(filename, img.thumb, img.transform, img.crs, img.nodata)
    assert os.path.exists(filename)

def test_write_geotif_nometadata(test_data, tmpdir):
    """Test write_geotif with missing metadata."""
    cache_dir = tmpdir.mkdir("cache")
    with open(test_data.dsm_pickled, "rb") as f:
        img = pickle.load(f)
    filename = os.path.join(cache_dir, 'outputs/test_out.geotif')
    array = np.asarray(img)
    with pytest.raises(RuntimeError):
        write_geotif(filename, array)
    