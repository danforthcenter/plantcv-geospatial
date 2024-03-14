# Read TIF File

import os 
import rasterio
#from plantcv.plantcv._debug import _debug
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.classes import Spectral_data, Params  
from plantcv.plantcv.hyperspectral.read_data import _make_pseudo_rgb

def read_geotif(filepath, mode="RGB"):
    """Read Georeferenced TIF image from file.

    Inputs:
    filepath: Path of the TIF image file.
    mode: Type of georeferenced image data 

    Returns:
    spectral_array: PlantCV format Spectral data object instance

    :param filepath: str
    :return spectral_array: __main__.Spectral_data
    """
    img = rasterio.open(filepath)
    height = img.height
    width = img.width
    mode_dict = {"RGB": {650: 0.0, 560: 1.0, 480: 2.0}, 
                 "BGR": {480: 0.0, 560: 1.0, 650: 2.0},
                 "RAW": {},  #BGR, Redgedge, NIR
                 "ALTUM": {650: 0.0, 560: 1.0, 480: 2.0, 717: 3.0, 842: 4.0},  #RGB, Redgedge, NIR
                 "PLANETLAB": {480: 0.0, 560: 1.0, 650: 2.0, 820: 4.0}}  #BGR, NIR
    wavelength_dict = mode_dict[mode.upper()]
    bands = img.count

    for i in (range(bands)):
        if i+1 == 1:
            stacked = img.read(i+1)
        else:
            band = img.read(i+1)
            stacked = np.dstack((stacked, band))
            
    spectral_array = Spectral_data(array_data=stacked,
                                   max_wavelength=None,
                                   min_wavelength=None,
                                   max_value=np.max(stacked), min_value=np.min(stacked),
                                   d_type=img.dtypes[0],
                                   wavelength_dict=wavelength_dict, samples=int(width),
                                   lines=int(height), interleave=None,
                                   wavelength_units="nm", array_type="datacube",
                                   pseudo_rgb=None, filename=filepath, default_bands=None)

    pseudo_rgb = _make_pseudo_rgb(spectral_array)
    spectral_array.pseudo_rgb = pseudo_rgb

    plot_image(img=pseudo_rgb)
    #_debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, str(params.device) + "_pseudo_rgb.png"))

    return spectral_array