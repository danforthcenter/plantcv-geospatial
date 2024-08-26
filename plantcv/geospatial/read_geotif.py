# Read georeferenced TIF files to Spectral Image data

import os
import cv2
import rasterio
import numpy as np
import fiona
from rasterio.mask import mask
from plantcv.plantcv import warn, params, fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.classes import Spectral_data
from shapely.geometry import shape, MultiPoint, mapping


def _find_closest_unsorted(array, target):
    """Find closest index of array item with smallest distance from
    the target
    Inputs:
    array:  list or array of wavelength labels
    target: target value
    Returns:
    idx:    index of closest value to the target
    :param array: numpy.ndarray
    :param target: int, float
    :return idx: int
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


def read_geotif(filename, bands="R,G,B", cropto=None):
    """Read Georeferenced TIF image from file.
    Inputs:
    filename:   Path of the TIF image file.
    bands:      Comma separated string representing the order of image bands
                (default bands="R,G,B"), or a list of wavelengths (e.g. bands=[650,560,480])
    cropto:     Path to a geoJSON-type shape file for cropping input image.
    Returns:
    spectral_array: PlantCV format Spectral data object instance
    :param filename: str
    :param bands: str, list
    :return spectral_array: __main__.Spectral_data
    """
    if cropto:
        with fiona.open(cropto, 'r') as shapefile:
            # polygon-type shapefile
            if len(shapefile) == 1:
                shapes = [feature['geometry'] for feature in shapefile]
            # points-type shapefile
            else:
                points = [shape(feature["geometry"]) for feature in shapefile]
                multi_point = MultiPoint(points)
                convex_hull = multi_point.convex_hull
                shapes = [mapping(convex_hull)]
        # rasterio does the cropping within open
        with rasterio.open(filename, 'r') as src:
            img_data, geo_transform = mask(src, shapes, crop=True)
            d_type = src.dtypes[0]
            geo_crs = src.crs.wkt

    else:
        img = rasterio.open(filename)
        img_data = img.read()
        d_type = img.dtypes[0]
        geo_transform = img.transform
        geo_crs = img.crs.wkt

    img_data = img_data.transpose(1, 2, 0)  # reshape such that z-dimension is last
    height, width, depth = img_data.shape
    wavelengths = {}

    # Parse bands if input is a string
    if isinstance(bands, str):
        bands = _parse_bands(bands)
    # Create a dictionary of wavelengths and their indices
    for i, wl in enumerate(bands):
        wavelengths[wl] = i
    # Check if user input matches image dimension in z direction
    if depth != len(bands):
        warn(f"{depth} bands found in the image data but {filename} was provided with {bands}")
    # Mask negative background values
    img_data[img_data < 0.] = 0
    if np.sum(img_data) == 0:
        fatal_error(f"your image is empty, are the crop-to bounds outside of the {filename} image area?")

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
                                   max_wavelength=None,
                                   min_wavelength=None,
                                   max_value=np.max(img_data), min_value=np.min(img_data),
                                   d_type=d_type,
                                   wavelength_dict=wavelengths, samples=int(width),
                                   lines=int(height), interleave=None,
                                   wavelength_units="nm", array_type="datacube",
                                   pseudo_rgb=pseudo_rgb, filename=filename,
                                   default_bands=[480, 540, 630],
                                   geo_transform=geo_transform,
                                   geo_crs=geo_crs)

    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir,
                                                    f"{params.device}_pseudo_rgb.png"))
    return spectral_array
