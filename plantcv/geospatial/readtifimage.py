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
                                   max_wavelength=float(str(header_dict["wavelength"][-1]).rstrip()),
                                   min_wavelength=float(str(header_dict["wavelength"][0]).rstrip()),
                                   max_value=max(inputarray), min_value=min(inputarray),
                                   d_type=header_dict["datatype"],
                                   wavelength_dict=wavelength_dict, samples=int(width),
                                   lines=int(height), interleave=header_dict["interleave"],
                                   wavelength_units="unknown", array_type="datacube",
                                   pseudo_rgb=None, filename=filepath, default_bands=None)

    return spectral_array
