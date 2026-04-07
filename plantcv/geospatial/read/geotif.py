# Read georeferenced TIF files to Spectral Image data

import os
import rasterio
import numpy as np
import fiona
from rasterio.mask import mask
from plantcv.plantcv import warn, params, fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.geospatial.images import GEO, DSM
from shapely.geometry import shape, MultiPoint, mapping
from plantcv.geospatial.read.netcdf import _read_to_class


def _parse_bands(bands):
    """Parse bands from a string or list into a list of wavelengths.

    Parameters
    ----------
    bands : str or list
        Comma-separated string of band symbols (e.g., ``"R,G,B"``) or a list
        of wavelengths.
        Currently Supported Band Symbols: R (650 nm), G (560 nm), B (480 nm),
        RE (717 nm), N (842 nm), NIR (842 nm), GRAY (0).

    Returns
    -------
    list
        List of wavelength values corresponding to the input bands.
    """
    if not isinstance(bands, str):
        return bands
    # Numeric list of bands
    band_list = []

    # Parse bands
    band_strs = bands.split(",")

    # Default values for symbolic bands
    default_wavelengths = {"R": 650, "G": 560, "B": 480, "RE": 717, "N": 842,
                           "NIR": 842, "GRAY": 0}

    for band in band_strs:
        # Check if the band symbols are supported
        if band.upper() not in default_wavelengths:
            fatal_error(f"Currently {band} is not supported, instead provide list of wavelengths in order.")
        # Append the default wavelength for each band
        band_list.append(default_wavelengths[band.upper()])

    return band_list


def _read_geotif_and_shapefile(filename, cropto):
    """Read Georeferenced TIF image from file and optionally crop to a
    shapefile boundary.

    Parameters
    ----------
    filename : str
        Path to the GeoTIF image file.
    cropto : str or None
        Path to the shapefile used to crop the image. If ``None``, the full
        image is read without cropping. Supports polygon-type shapefiles
        (single feature) and point-type shapefiles (convex hull is computed).

    Returns
    -------
    img_data : numpy.ndarray
        Image data array with shape ``(bands, height, width)``.
    metadata : dict
        Rasterio metadata dictionary including CRS, transform, and driver
        information.
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
            img_data, trans_metadata = mask(src, shapes, crop=True)
            metadata = src.meta.copy()
            metadata.update({"transform": trans_metadata})
    else:
        with rasterio.open(filename, 'r') as img:
            img_data = img.read()
            metadata = img.meta.copy()

    return img_data, metadata


def geotif(filename, bands="R,G,B", cropto=None, cutoff=None):
    """Read Georeferenced TIF image from file.

    Parameters
    ----------
    filename : str
        Path of the TIF image file.
    bands : str or list, optional
        Comma-separated string listing the order of bands (e.g., "R,G,B") or a
        list of wavelengths.
        Supported band symbols: R, G, B, RE, N, NIR, GRAY. Default is "R,G,B".
    cropto : str, optional
        Path of the shapefile to crop the image. Default is None.
    cutoff : float, optional
        Percentile above which to remove points (only used for grayscale
        images). Default is None.

    Returns
    -------
    plantcv.plantcv.classes.Spectral_data
        Orthomosaic image data in a Spectral_data class instance.
    """
    # Read the geotif image and shapefile for cropping
    img_data, metadata = _read_geotif_and_shapefile(filename, cropto)
    # reshape such that z-dimension is last
    img_data = img_data.transpose(1, 2, 0)
    _, _, depth = img_data.shape
    # Check for mask
    mask_layer = None
    for i in range(depth):
        if len(np.unique(img_data[:, :, [i]])) == 2:
            mask_layer = img_data[:, :, [i]]
            img_data = np.delete(img_data, i, 2)
    # reset depth in case the image data was changed
    _, _, depth = img_data.shape
    # Parse bands
    bands = _parse_bands(bands)
    # Check if user input matches image dimension in z direction
    if depth > len(bands):
        warn(f"{depth} bands found in the image data but {filename} was provided with {bands}")
    if depth < len(bands):
        fatal_error("your image depth is less than the specified number of bands")
    if len(np.unique(img_data)) == 1:
        # If totally uniform then indicates image only contains no-data value
        fatal_error(f"your image is empty, are the crop-to bounds outside of the {filename} image area?")

    # Apply mask layer if it exists
    if mask_layer is not None:
        img_data = np.where(mask_layer == 0, 0, img_data)

    # Check if img is uint16
    if img_data.dtype == "uint16":
        img_data = ((img_data/65535.0) * 255.0).astype(np.uint8)

    obj = _read_to_class(depth, img_data, filename, bands, metadata["crs"],
                         metadata["transform"], metadata["nodata"], cutoff)

    _debug(visual=obj.thumb,
           filename=os.path.join(params.debug_outdir, f"{params.device}_thumbnail.png"))
    return obj
