# Read TIF File

import os 
import cv2
import rasterio
import numpy as np 
#from plantcv.plantcv._debug import _debug
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.classes import Spectral_data  
from plantcv.plantcv.hyperspectral.read_data import _make_pseudo_rgb

def read_geotif(filepath, bands="R,G,B"):
    """Read Georeferenced TIF image from file.

    Inputs:
    filepath: Path of the TIF image file.
    bands: Comma separated string representing the order of image bands (default bands="R,G,B")

    Returns:
    spectral_array: PlantCV format Spectral data object instance

    :param filepath: str
    :param bands: str
    :return spectral_array: __main__.Spectral_data
    """
    img = rasterio.open(filepath)
    img_data = img.read()
    img_data = img_data.transpose(1, 2, 0)  # reshape such that z-dimension is last 
    height = img.height
    width = img.width
    wavelengths = [] 

    # Parse bands
    list_bands = bands.split(",") 
    default_wavelengths = {"R": 650, "G": 560, "B": 480, "RE":717, "N": 842, "NIR": 842}
    for i, band in enumerate(list_bands):
        wavelength = default_wavelengths[band.upper()]
        wavelengths[wavelength] = i
    bands = img.count

    # Make a Spectral_data instance before calculating a pseudo-rgb 
    spectral_array = Spectral_data(array_data=img_data,
                                   max_wavelength=None,
                                   min_wavelength=None,
                                   max_value=np.max(img_data), min_value=np.min(img_data),
                                   d_type=img.dtypes[0],
                                   wavelength_dict=wavelengths, samples=int(width),
                                   lines=int(height), interleave=None,
                                   wavelength_units="nm", array_type="datacube",
                                   pseudo_rgb=None, filename=filepath, default_bands=None)

    pseudo_rgb = _make_pseudo_rgb(spectral_array)
    spectral_array.pseudo_rgb = pseudo_rgb

    plot_image(img=pseudo_rgb)
    #_debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, str(params.device) + "_pseudo_rgb.png"))

    return spectral_array
