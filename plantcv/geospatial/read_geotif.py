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


def read_geotif(filename, bands="R,G,B"):
    """Read Georeferenced TIF image from file.

    Parameters
    ----------
    filename : str
        Path of the TIF image file.
    bands : str, list, optional
        Comma separated string listing the order of bands or a list of wavelengths, by default "R,G,B"

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

    if isinstance(bands, str):
        # Parse bands
        list_bands = bands.split(",")
        default_wavelengths = {"R": 650, "G": 560, "B": 480, "RE": 717, "N": 842, "NIR": 842}

        for i, band in enumerate(list_bands):
            # Check if the band symbols are supported
            if band.upper() not in default_wavelengths:
                fatal_error(f"Currently {band} is not supported, instead provide list of wavelengths in order.")
            wavelength = default_wavelengths[band.upper()]
            wavelengths[wavelength] = i

    elif isinstance(bands, list):
        for i, wl in enumerate(bands):
            wavelengths[wl] = i

    # If RGB image then should be uint8, skip
    if len(list_bands) == 3:
        # Create with first three bands
        rgb_img = img_data[:, :, :3]
        spectral_array = rgb_img.astype('uint8')
        spectral_array = cv2.cvtColor(spectral_array, cv2.COLOR_BGR2RGB)
        # Drop 4th band if there is one and then retun that as numpy array
        _debug(visual=spectral_array,
               filename=os.path.join(params.debug_outdir, str(params.device) + "pseudo_rgb.png"))

    else:
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
        pseudo_rgb = pseudo_rgb.astype('float32') ** (1 / 2.2)
        pseudo_rgb = pseudo_rgb * 255
        pseudo_rgb = pseudo_rgb.astype('uint8')
        # Make a Spectral_data instance before calculating a pseudo-rgb
        spectral_array = Spectral_data(array_data=img_data,
                                       max_wavelength=None,
                                       min_wavelength=None,
                                       max_value=np.max(img_data), min_value=np.min(img_data),
                                       d_type=img.dtypes[0],
                                       wavelength_dict=wavelengths, samples=int(width),
                                       lines=int(height), interleave=None,
                                       wavelength_units="nm", array_type="datacube",
                                       pseudo_rgb=pseudo_rgb, filename=filename, default_bands=None)

        _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir,
                                                        str(params.device) + "pseudo_rgb.png"))
    return spectral_array
