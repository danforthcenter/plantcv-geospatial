# Read georeferenced TIF files to Spectral Image data

import os
import cv2
import rasterio
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.classes import Spectral_data


def _find_closest_unsorted(array, target):
    """Find closest index of array item with smallest distance from the target.

    Parameters
    ----------
    array : numpy.ndarray
        Array of wavelength labels
    target : int, float
        Target value

    Returns
    -------
    int
        Index of closest value to the target
    """
    return min(range(len(array)), key=lambda i: abs(array[i]-target))


def _parse_bands(bands):
    """Parse bands.

    Parameters
    ----------
    bands : str
        Comma separated string listing the order of bands

    Returns
    -------
    list
        List of bands
    """
    # Numeric list of bands
    band_list = []

    # Parse bands
    band_strs = bands.split(",")

    # Default values for symbolic bands
    default_wavelengths = {"R": 650, "G": 560, "B": 480, "RE": 717, "N": 842, "NIR": 842}

    for band in band_strs:
        # Check if the band symbols are supported
        if band.upper() not in default_wavelengths:
            fatal_error(f"Currently {band} is not supported, instead provide list of wavelengths in order.")
        # Append the default wavelength for each band
        band_list.append(default_wavelengths[band.upper()])

    return band_list


def read_geotif(filename, bands="B,G,R"):
    """Read Georeferenced TIF image from file.

    Parameters
    ----------
    filename : str
        Path of the TIF image file.
    bands : str, list, optional
        Comma separated string listing the order of bands or a list of wavelengths, by default "B,G,R"

    Returns
    -------
    plantcv.plantcv.classes.Spectral_data
        Orthomosaic image data
    """
    img = rasterio.open(filename)
    img_data = img.read()
    img_data = img_data.transpose(1, 2, 0)  # reshape such that z-dimension is last
    height = img.height
    width = img.width
    wavelengths = {}

    # Parse bands if input is a string
    if isinstance(bands, str):
        bands = _parse_bands(bands)

    # Create a dictionary of wavelengths and their indices
    for i, wl in enumerate(bands):
        wavelengths[wl] = i

    # Mask negative background values
    img_data[img_data < 0.] = 0
    # Make a list of wavelength keys
    wl_keys = wavelengths.keys()
    # Find which bands to use for red, green, and blue bands of the pseudo_rgb image
    id_red = _find_closest_unsorted(array=np.array([float(i) for i in wl_keys]), target=630)
    id_green = _find_closest_unsorted(array=np.array([float(i) for i in wl_keys]), target=540)
    id_blue = _find_closest_unsorted(array=np.array([float(i) for i in wl_keys]), target=480)
    # Stack bands together, BGR since plot_image will convert BGR2RGB automatically
    pseudo_rgb = cv2.merge((img_data[:, :, [id_blue]],
                            img_data[:, :, [id_green]],
                            img_data[:, :, [id_red]]))
    # Gamma correction
    if pseudo_rgb.dtype != 'uint8':
        pseudo_rgb = pseudo_rgb.astype('float32') ** (1 / 2.2)
        pseudo_rgb = pseudo_rgb * 255
        pseudo_rgb = pseudo_rgb.astype('uint8')

    # Make a Spectral_data instance before calculating a pseudo-rgb
    spectral_array = Spectral_data(array_data=img_data,
                                   max_wavelength=max(wavelengths, key=wavelengths.get),
                                   min_wavelength=min(wavelengths, key=wavelengths.get),
                                   max_value=np.max(img_data), min_value=np.min(img_data),
                                   d_type=img.dtypes[0],
                                   wavelength_dict=wavelengths, samples=int(width),
                                   lines=int(height), interleave=None,
                                   wavelength_units="nm", array_type="datacube",
                                   pseudo_rgb=pseudo_rgb, filename=filename, default_bands=[480, 540, 630])

    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, f"{params.device}_pseudo_rgb.png"))

    return spectral_array
