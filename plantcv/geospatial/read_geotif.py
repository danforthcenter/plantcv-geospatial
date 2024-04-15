import rasterio
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv.hyperspectral.read_data import _make_pseudo_rgb
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.classes import Spectral_data


def read_geotif(filename, bands="R,G,B"):
    """Read Georeferenced TIF image from file.

    Inputs:
    filename:   Path of the TIF image file.
    bands:      Comma separated string representing the order of image bands (default bands="R,G,B"),
                or a list of wavelengths (e.g. bands=[650,560,480])

    Returns:
    spectral_array: PlantCV format Spectral data object instance

    :param filename: str
    :param bands: str, list
    :return spectral_array: __main__.Spectral_data
    """
    img = rasterio.open(filename)
    img_data = img.read()
    img_data = img_data.transpose(1, 2, 0)  # reshape such that z-dimension is last
    height = img.height
    width = img.width
    wavelengths = {}

    if isinstance(bands, str):
        print("string of bands processing...")
        # Parse bands
        list_bands = bands.split(",")
        default_wavelengths = {"R": 650, "G": 560, "B": 480, "RE": 717, "N": 842, "NIR": 842}
        wavelength_keys = default_wavelengths.keys()

        for i, band in enumerate(list_bands):

            if band.upper() not in wavelength_keys:
                fatal_error(f"Currently {band} is not supported, instead provide list of wavelengths in order.")
            else:
                wavelength = default_wavelengths[band.upper()]
                wavelengths[wavelength] = i

    elif isinstance(bands, list):
        print("List of bands processing...")
        for i, wl in enumerate(bands):
            wavelengths[wl] = i

    # Make a Spectral_data instance before calculating a pseudo-rgb
    spectral_array = Spectral_data(array_data=img_data,
                                   max_wavelength=None,
                                   min_wavelength=None,
                                   max_value=np.max(img_data), min_value=np.min(img_data),
                                   d_type=img.dtypes[0],
                                   wavelength_dict=wavelengths, samples=int(width),
                                   lines=int(height), interleave=None,
                                   wavelength_units="nm", array_type="datacube",
                                   pseudo_rgb=None, filename=filename, default_bands=None)

    pseudo_rgb = _make_pseudo_rgb(spectral_array)
    pseudo_rgb = pseudo_rgb.astype('float32')
    plot_image(img=pseudo_rgb)  # Replace with _debug

    return spectral_array
