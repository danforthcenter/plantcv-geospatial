# Read TIF File
import rasterio
from plantcv.plantcv.classes import Spectral_data 

def readimage(filepath):
    """Read TIF image from file.

    Inputs:
    filepath: Path of the TIF image file.

    Returns:
    spectral_array: PlantCV format Hyperspectral data instance

    :param filepath: str
    :return spectral_array: __main__.Spectral_data
    """
    img = rasterio.open(filepath)
    inputarray = img.read()
    height = img.height
    width = img.width
    bands = img.count
    spectral_array = Spectral_data(array_data=inputarray,
                                   max_wavelength=None,
                                   min_wavelength=None,
                                   max_value=max(inputarray), min_value=min(inputarray),
                                   d_type=img.dtypes[0],
                                   wavelength_dict={}, samples=int(width),
                                   lines=int(height), interleave=None,
                                   wavelength_units="unknown", array_type="datacube",
                                   pseudo_rgb=None, filename=filepath, default_bands=None)

    return spectral_array
