"""Tests for geospatial.rgb_index."""

import numpy as np
from plantcv.geospatial import read_geotif, rgb_index, list_rgb_indices


def test_geospatial_rgb_index_names():
    """Test supported RGB index names."""
    assert list_rgb_indices() == (
        "BI", "SCI", "GLI", "HI", "NGRDI", "SI", "VARI", "HUE",
        "BG_RATIO", "BGI", "VI", "CI"
    )


def test_geospatial_rgb_index_formulas(test_data):
    """Test RGB index formulas against expected calculations."""
    eps = 1e-5
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    pseudo = img.pseudo_rgb.astype(np.float32)
    b_channel = pseudo[:, :, 0]
    g_channel = pseudo[:, :, 1]
    r_channel = pseudo[:, :, 2]

    expected = {
        "BI": np.sqrt((r_channel**2 + g_channel**2 + b_channel**2) / 3.0),
        "SCI": (r_channel - g_channel) / (r_channel + g_channel + eps),
        "GLI": (2 * g_channel - r_channel - b_channel) / (2 * g_channel + r_channel + b_channel + eps),
        "HI": (2 * r_channel - g_channel - b_channel) / (g_channel - b_channel + eps),
        "NGRDI": (g_channel - r_channel) / (g_channel + r_channel + eps),
        "SI": (r_channel - b_channel) / (r_channel + b_channel + eps),
        "VARI": (g_channel - r_channel) / (g_channel + r_channel - b_channel + eps),
        "HUE": np.arctan((2 * (b_channel - g_channel - r_channel) / 30.5) * (g_channel - r_channel)),
        "BG_RATIO": b_channel / (g_channel + eps),
        "BGI": (g_channel - b_channel) / (g_channel + b_channel + eps),
        "VI": g_channel - ((b_channel + r_channel) / 2.0),
        "CI": (g_channel / (r_channel + eps)) - 1.0,
    }

    for name in list_rgb_indices():
        observed = rgb_index(img=img, index=name)
        assert np.allclose(observed, expected[name], equal_nan=True)
