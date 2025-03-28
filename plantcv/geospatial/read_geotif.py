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


def _read_geotif_and_shapefile(filename, cropto):
    """Read Georeferenced TIF image from file and shapefile for cropping.

    Parameters
    ----------
    filename : str
        Path of the TIF image file.
    cropto : str
        Path of the shapefile to crop the image

    Returns
    -------
    tuple
        Tuple of image data, geotransform, data type, and crs
    """
    if cropto:
        with fiona.open(cropto, 'r') as shapefile:
            # polygon-type shapefile
            if len(shapefile) == 1:
                shapes = [feature['geometry'] for feature in shapefile]
            # points-type shapefile
            if len(shapefile) != 1:
                points = [shape(feature["geometry"]) for feature in shapefile]
                multi_point = MultiPoint(points)
                convex_hull = multi_point.convex_hull
                shapes = [mapping(convex_hull)]
        # rasterio does the cropping within open
        with rasterio.open(filename, 'r') as src:
            img_data, trans_metadata = mask(src, shapes, crop=True)
            metadata = src.meta.copy()
            metadata.update({"transform": trans_metadata})
            d_type = src.dtypes[0]

    else:
        img = rasterio.open(filename)
        img_data = img.read()
        d_type = img.dtypes[0]
        metadata = img.meta.copy()

    return img_data, d_type, metadata


def read_geotif(filename, bands="R,G,B", cropto=None):
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
        Orthomosaic image data in a Spectral_data class instance
    """
    # Read the geotif image and shapefile for cropping
    img_data, d_type, metadata = _read_geotif_and_shapefile(filename, cropto)

    img_data = img_data.transpose(1, 2, 0)  # reshape such that z-dimension is last
    height, width, depth = img_data.shape
    wavelengths = {}

    # Check for mask
    mask_layer = None
    for i in range(depth):
        if len(np.unique(img_data[:, :, [i]])) == 2:
            mask_layer = img_data[:, :, [i]]
            img_data = np.delete(img_data, i, 2)

    # Parse bands if input is a string
    if isinstance(bands, str):
        bands = _parse_bands(bands)
    # Create a dictionary of wavelengths and their indices
    for i, wl in enumerate(bands):
        wavelengths[wl] = i
    # Check if user input matches image dimension in z direction
    if depth != len(bands):
        warn(f"{depth} bands found in the image data but {filename} was provided with {bands}")
    if depth < len(bands):
        fatal_error("your image depth is less than the specified number of bands")
    # Mask negative background values
    img_data[img_data < 0.] = 0
    if np.sum(img_data) == 0:
        fatal_error(f"your image is empty, are the crop-to bounds outside of the {filename} image area?")
    # Make a list of wavelength keys
    if mask_layer is not None:
        img_data = np.where(mask_layer == 0, 0, img_data)
    # Find which bands to use for red, green, and blue bands of the pseudo_rgb image
    id_red = _find_closest_unsorted(array=np.array([float(i) for i in wavelengths]), target=630)
    id_green = _find_closest_unsorted(array=np.array([float(i) for i in wavelengths]), target=540)
    id_blue = _find_closest_unsorted(array=np.array([float(i) for i in wavelengths]), target=480)
    # Stack bands together, BGR since plot_image will convert BGR2RGB automatically
    pseudo_rgb = cv2.merge((img_data[:, :, [id_blue]],
                            img_data[:, :, [id_green]],
                            img_data[:, :, [id_red]]))
    # Gamma correction
    # if pseudo_rgb.dtype != 'uint8':
    #     pseudo_rgb = pseudo_rgb.astype('float32') ** (1 / 2.2)
    #     pseudo_rgb = pseudo_rgb * 255
    #     pseudo_rgb = pseudo_rgb.astype('uint8')
    pseudo_rgb = pseudo_rgb.astype('uint8')
    # Make a Spectral_data instance before calculating a pseudo-rgb
    spectral_array = Spectral_data(array_data=img_data,
                                   max_wavelength=max(wavelengths, key=wavelengths.get),
                                   min_wavelength=min(wavelengths, key=wavelengths.get),
                                   max_value=np.max(img_data), min_value=np.min(img_data),
                                   d_type=d_type,
                                   wavelength_dict=wavelengths, samples=int(width),
                                   lines=int(height), interleave=None,
                                   wavelength_units="nm", array_type="datacube",
                                   pseudo_rgb=pseudo_rgb, filename=filename,
                                   default_bands=[480, 540, 630],
                                   metadata=metadata)

    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, f"{params.device}_pseudo_rgb.png"))
    return spectral_array
