"""Tests for geospatial.resize"""

import dill as pickle
#import numpy as np
#import pytest
from plantcv.plantcv import params
from plantcv.geospatial import GEO, DSM
from plantcv.geospatial.resize import resize


def test_resize_geo(test_data):
    """Test resize with a GEO object preserves class and metadata."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    params.debug = None
    resized = resize(img=img, size=(100, 100))
    assert isinstance(resized, GEO)
    assert resized.shape[:2] == (100, 100)
    assert resized.wavelengths == img.wavelengths
    assert resized.default_wavelengths == img.default_wavelengths
    assert resized.crs == img.crs
    assert resized.nodata == getattr(img, "nodata", None)


#def test_resize_geo_updates_transform(test_data):
#    """Test resize with a GEO object scales the affine transform correctly."""
#    with open(test_data.geo_pickled, "rb") as f:
#        img = pickle.load(f)
#    params.debug = None
#    orig_h, orig_w = img.shape[:2]
#    new_w, new_h = orig_w // 2, orig_h // 2
#    resized = resize(img=img, size=(new_w, new_h))
#    if img.transform is not None:
#        assert resized.transform.a == pytest.approx(img.transform.a * (orig_w / new_w))
#        assert resized.transform.e == pytest.approx(img.transform.e * (orig_h / new_h))
#        assert resized.transform.c == pytest.approx(img.transform.c)
#        assert resized.transform.f == pytest.approx(img.transform.f)


def test_resize_dsm(test_data):
    """Test resize with a DSM object preserves class and metadata."""
    with open(test_data.dsm_pickled, "rb") as f:
        img = pickle.load(f)
    params.debug = None
    resized = resize(img=img, size=(50, 50))
    assert isinstance(resized, DSM)
    assert resized.shape[:2] == (50, 50)
    assert resized.crs == img.crs
    assert resized.cutoff == getattr(img, "cutoff", None)
    assert resized.nodata == getattr(img, "nodata", None)


#def test_resize_image():
#    """Test resize with a plain Image object."""
#    params.debug = None
#    img = Image(input_array=np.zeros((100, 200), dtype=np.uint8), filename="test.png")
#    resized = resize(img=img, size=(50, 50))
#    assert isinstance(resized, Image)
#    assert resized.shape == (50, 50)
#    assert resized.filename == "test.png"


#def test_resize_no_interpolation(test_data):
#    """Test resize with interpolation=None uses crop/pad mode."""
#    with open(test_data.geo_pickled, "rb") as f:
#        img = pickle.load(f)
#    params.debug = None
#    resized = resize(img=img, size=(100, 100), interpolation=None)
#    assert isinstance(resized, GEO)
#    assert resized.shape[:2] == (100, 100)


#def test_resize_none_transform():
#    """Test resize with a GEO object that has no affine transform."""
#    params.debug = None
#    geo = GEO(
#        input_array=np.zeros((100, 100, 3), dtype=np.uint8),
#        filename="test.tif",
#        wavelengths=[480, 540, 630],
#        default_wavelengths=[480, 540, 630],
#        crs=None,
#        transform=None,
#        nodata=None
#    )
#    resized = resize(img=geo, size=(50, 50))
#    assert isinstance(resized, GEO)
#    assert resized.transform is None
