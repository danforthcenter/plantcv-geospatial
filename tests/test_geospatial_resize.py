"""Tests for geospatial.resize"""

import dill as pickle
import numpy as np
import pytest
from plantcv.geospatial import GEO, DSM
from plantcv.geospatial.resize import resize


def test_resize_geo(test_data):
    """Test resize with a GEO object preserves class and metadata."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    resized = resize(img=img, size=(100, 100))
    assert isinstance(resized, GEO)
    assert resized.shape[:2] == (100, 100)
    assert resized.wavelengths == img.wavelengths
    assert resized.default_wavelengths == img.default_wavelengths
    assert resized.crs == img.crs
    assert resized.nodata == getattr(img, "nodata", None)


def test_resize_dsm(test_data):
    """Test resize with a DSM object preserves class and metadata."""
    with open(test_data.dsm_pickled, "rb") as f:
        img = pickle.load(f)
    img.nodata = 0
    resized = resize(img=img, size=(50, 50))
    assert isinstance(resized, DSM)
    assert resized.shape[:2] == (50, 50)
    assert resized.crs == img.crs
    assert resized.cutoff == getattr(img, "cutoff", None)
    assert resized.nodata == getattr(img, "nodata", None)


def test_resize_none_transform():
    """Test resize with a GEO object that has no affine transform."""
    geo = GEO(
        input_array=np.zeros((100, 100, 3), dtype=np.uint8),
        filename="test.tif",
        wavelengths=[480, 540, 630],
        default_wavelengths=[480, 540, 630],
        crs=None,
        transform=None,
        nodata=0
    )
    resized = resize(img=geo, size=(50, 50))
    assert isinstance(resized, GEO)
    assert resized.transform is None

def test_resize_geo_multiband():
    """Test resize with a GEO object with more than 4 bands."""
    arr = np.zeros((50, 50, 5), dtype=np.uint8)
    geo = GEO(
        input_array=arr,
        filename="test.tif",
        wavelengths=[650, 560, 480, 717, 842],
        default_wavelengths=[480, 560, 650],
        crs=None,
        transform=None,
        nodata=None
    )
    resized = resize(img=geo, size=(25, 25))
    assert isinstance(resized, GEO)
    assert resized.shape == (25, 25, 5)


def test_resize_wrong_input():
    """Test resize with non-geospatial array."""
    input_array=np.zeros((100, 100, 3), dtype=np.uint8)
    with pytest.raises(RuntimeError):
        _ = resize(img=input_array, size=(50, 50))
