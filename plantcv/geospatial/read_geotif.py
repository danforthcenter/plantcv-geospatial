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
    dims_found = len(bands.split(","))
    height, width, depth = img_data.shape
    if depth != dims_found:
        warn(f"{depth} bands found in the image data but the function was provided with {dims_found}")
    wavelengths = {}

    if isinstance(bands, str):
        # Parse bands
        list_bands = bands.split(",")
        default_wavelengths = {"R": 650, "G": 560, "B": 480, "RE": 717, "N": 842, "NIR": 842}
        wavelength_keys = default_wavelengths.keys()

        for i, band in enumerate(list_bands):

            if band.upper() not in wavelength_keys:
                fatal_error(f"Currently {band} is not supported")
            else:
                wavelength = default_wavelengths[band.upper()]
                wavelengths[wavelength] = i

    elif isinstance(bands, list):
        # Keep list_bands to check length in next section
        list_bands = bands
        for i, wl in enumerate(bands):
            wavelengths[wl] = i

    # If RGB image then should be uint8, skip
    if len(list_bands) == 3:
        # Create with first three bands
        rgb_img = img_data[:, :, :3]
        temp_img = rgb_img.astype('uint8')
        pseudo_rgb = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
        img_data = pseudo_rgb

    else:
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
    if pseudo_rgb.dtype != 'uint8':
        # Gamma correction
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
                                   pseudo_rgb=pseudo_rgb, filename=filename, default_bands=None,
                                   geo_transform=geo_transform,
                                   geo_crs=geo_crs)

    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir,
                                                    str(params.device) + "pseudo_rgb.png"))
    return spectral_array
