"""Tests for geospatial.split_rgb_channels."""

import numpy as np
from plantcv.geospatial import read_geotif, split_rgb_channels


def test_geospatial_split_rgb_channels(test_data):
    """Test channel splitting for pseudo_rgb images."""
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")

    r_channel, g_channel, b_channel = split_rgb_channels(img=img)

    assert r_channel.shape == img.pseudo_rgb[:, :, 2].shape
    assert g_channel.shape == img.pseudo_rgb[:, :, 1].shape
    assert b_channel.shape == img.pseudo_rgb[:, :, 0].shape

    assert (r_channel == img.pseudo_rgb[:, :, 2]).all()
    assert (g_channel == img.pseudo_rgb[:, :, 1]).all()
    assert (b_channel == img.pseudo_rgb[:, :, 0]).all()
    assert r_channel.dtype == np.float32
    assert g_channel.dtype == np.float32
    assert b_channel.dtype == np.float32


def test_geospatial_split_rgb_channels_original_dtype(test_data):
    """Test optional original dtype output."""
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")

    r_channel, g_channel, b_channel = split_rgb_channels(img=img, as_float=False)

    assert r_channel.dtype == img.pseudo_rgb.dtype
    assert g_channel.dtype == img.pseudo_rgb.dtype
    assert b_channel.dtype == img.pseudo_rgb.dtype
