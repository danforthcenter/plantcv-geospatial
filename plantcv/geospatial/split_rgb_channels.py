# Split pseudo_rgb channels into red, green, and blue images

import os
import numpy as np
from plantcv.plantcv import fatal_error, params
from plantcv.plantcv._debug import _debug


def split_rgb_channels(img, as_float=True):
    """Split a geospatial pseudo-RGB image into red, green, and blue channels.

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        A spectral image object returned by ``read_geotif`` or ``read_netcdf``.
    as_float : bool
        If ``True`` (default), return channels as ``numpy.float32`` for index
        math. If ``False``, return channels in their original dtype.

    Returns
    -------
    tuple of numpy.ndarray
        ``(r_channel, g_channel, b_channel)`` grayscale channel images.
    """
    pseudo_rgb = img.pseudo_rgb

    if pseudo_rgb is None:
        fatal_error("Input image does not contain pseudo_rgb data.")

    if len(pseudo_rgb.shape) != 3 or pseudo_rgb.shape[2] != 3:
        fatal_error("Input pseudo_rgb image must have exactly 3 channels.")

    b_channel = pseudo_rgb[:, :, 0]
    g_channel = pseudo_rgb[:, :, 1]
    r_channel = pseudo_rgb[:, :, 2]

    if as_float:
        r_channel = r_channel.astype(np.float32)
        g_channel = g_channel.astype(np.float32)
        b_channel = b_channel.astype(np.float32)

    _debug(visual=r_channel,
           filename=os.path.join(params.debug_outdir, f"{params.device}_red_channel.png"),
           cmap='gray')
    _debug(visual=g_channel,
           filename=os.path.join(params.debug_outdir, f"{params.device}_green_channel.png"),
           cmap='gray')
    _debug(visual=b_channel,
           filename=os.path.join(params.debug_outdir, f"{params.device}_blue_channel.png"),
           cmap='gray')

    return r_channel, g_channel, b_channel
