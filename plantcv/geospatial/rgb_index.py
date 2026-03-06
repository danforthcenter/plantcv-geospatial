# Calculate RGB-based vegetation and color indices from geospatial pseudo_rgb

import os
import numpy as np
from plantcv.plantcv import fatal_error, params
from plantcv.plantcv._debug import _debug
from plantcv.geospatial.split_rgb_channels import split_rgb_channels


_RGB_INDEX_NAMES = (
    "BI", "SCI", "GLI", "HI", "NGRDI", "SI", "VARI", "HUE",
    "BG_RATIO", "BGI", "VI", "CI"
)


def list_rgb_indices():
    """List supported RGB index names.

    Returns
    -------
    tuple
        Supported RGB index abbreviations.
    """
    return _RGB_INDEX_NAMES


def rgb_index(img, index, eps=1e-5):
    """Calculate an RGB index from a geospatial pseudo-RGB image.

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        A spectral image object returned by ``read_geotif`` or ``read_netcdf``.
    index : str
        RGB index abbreviation. Supported values:
        ``BI``, ``SCI``, ``GLI``, ``HI``, ``NGRDI``, ``SI``, ``VARI``,
        ``HUE``, ``BG_RATIO``, ``BGI``, ``VI``, ``CI``.
    eps : float
        Small value added to denominators to avoid divide-by-zero.

    Returns
    -------
    numpy.ndarray
        Calculated index image.
    """
    name = str(index).upper()
    if name not in _RGB_INDEX_NAMES:
        fatal_error(
            f"Unsupported RGB index '{index}'. "
            f"Supported indices: {', '.join(_RGB_INDEX_NAMES)}"
        )

    r_channel, g_channel, b_channel = split_rgb_channels(img=img, as_float=True)

    with np.errstate(divide='ignore', invalid='ignore'):
        if name == "BI":
            index_img = np.sqrt((r_channel**2 + g_channel**2 + b_channel**2) / 3.0)
        elif name == "SCI":
            index_img = (r_channel - g_channel) / (r_channel + g_channel + eps)
        elif name == "GLI":
            index_img = (2 * g_channel - r_channel - b_channel) / (
                2 * g_channel + r_channel + b_channel + eps
            )
        elif name == "HI":
            index_img = (2 * r_channel - g_channel - b_channel) / (g_channel - b_channel + eps)
        elif name == "NGRDI":
            index_img = (g_channel - r_channel) / (g_channel + r_channel + eps)
        elif name == "SI":
            index_img = (r_channel - b_channel) / (r_channel + b_channel + eps)
        elif name == "VARI":
            index_img = (g_channel - r_channel) / (g_channel + r_channel - b_channel + eps)
        elif name == "HUE":
            # Follows FIELDimageR expression exactly: atan(2*(B-G-R)/30.5*(G-R))
            index_img = np.arctan(
                (2 * (b_channel - g_channel - r_channel) / 30.5) *
                (g_channel - r_channel)
            )
        elif name == "BG_RATIO":
            index_img = b_channel / (g_channel + eps)
        elif name == "BGI":
            index_img = (g_channel - b_channel) / (g_channel + b_channel + eps)
        elif name == "VI":
            index_img = g_channel - ((b_channel + r_channel) / 2.0)
        elif name == "CI":
            index_img = (g_channel / (r_channel + eps)) - 1.0
        else:
            fatal_error(
                f"Unsupported RGB index '{index}'. "
                f"Supported indices: {', '.join(_RGB_INDEX_NAMES)}"
            )

    _debug(visual=index_img,
           filename=os.path.join(params.debug_outdir, f"{params.device}_{name.lower()}_index.png"),
           cmap='gray')

    return index_img
