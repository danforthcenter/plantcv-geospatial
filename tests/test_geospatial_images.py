"""Tests for geospatial.images"""

import numpy as np
from plantcv.geospatial import Image, GEO, DSM

def test_image():
    """Test creating an Image class image."""
    img = Image(input_array=np.zeros((10, 10), dtype=np.uint8), filename="image.png")
    assert isinstance(img, Image)

def test_image_none():
    """Test creating an Image class image."""
    img = Image(input_array=None, filename=None)
    assert isinstance(img, Image)

def test_image_slice():
    """Test subsetting an Image."""
    img = Image(input_array=np.zeros((10, 10), dtype=np.uint8), filename="image.png")
    assert img[0:5, 0:5].shape == (5, 5)

def test_geo():
    """Test creating a GEO class image."""
    geo = GEO(input_array=np.zeros((10, 10, 3), dtype=np.uint8), filename="geo.tif", 
              wavelengths=[630, 540, 480],
              default_wavelengths=[480, 540, 630], crs = None, 
              transform = None)
    assert isinstance(geo, GEO)

def test_dsm():
    """Test creating a DSM class image."""
    dsm = DSM(input_array=np.zeros((10, 10), dtype=np.float32), filename="dsm.tif", 
              crs = None, transform = None, cutoff = 1.0)
    assert isinstance(dsm, DSM)
