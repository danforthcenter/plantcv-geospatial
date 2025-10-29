# Read NASA-formatted netCDF files to Spectral Image data

import netCDF4 as nc
import numpy as np
import cv2
import os
import rasterio
from plantcv.plantcv import params, transform
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.classes import Spectral_data
from plantcv.geospatial.read_geotif import _find_closest_unsorted
from geopandas import GeoDataFrame


def _combine_bands(ds):
    """Combine bands from individual netCDF variables.

    Parameters
    ----------
    ds : netCDF dataset read in with netCDF4 package

    Returns
    -------
    fullmat : numpy ndarray
        Array of combined data from all bands
    wavelengths : dictionary
        Dictionary of wavelengths
    """
    # Pull all available wavelengths using name of variable
    params_set = params.debug
    params.debug = None
    bands = []
    wavelengths = {}
    for idx, i in enumerate(ds.groups['geophysical_data'].variables):
        if i[0:4] == "rhos":
            bands.append(i)
            wavelengths[i.split("_")[1]] = idx
    # Make a list of the dataframe for each wavelength
    channels = []
    for i in bands:
        temp = np.array(ds.groups['geophysical_data'].variables[i][:])
        temp[temp == np.min(temp)] = 0
        rescaled = transform.rescale(temp)
        channels.append(rescaled)
    # Combine wavelenghts into one cube
    fullmat = cv2.merge(channels)

    params.debug = params_set
    return fullmat, wavelengths


def _crop_allbands(fulldf, ds, bounds):
    """Crop combined data frame with all bands to min/max coordinates.

    Parameters
    ----------
    fulldf : numpy ndarray
        Combined data frame of all bands
    ds : netCDF dataset read in with netCDF4 package
    bounds : list
        List of min/max latitude and longitude to crop to

    Returns
    -------
    fulldf_cropped : numpy ndarray
        Combine bands data frame cropped to bounds
    lat_cropped : numpy ndarray
        Cropped latitude data frame
    lon_cropped : numpy ndarray
        Cropped longitutde data frame
    """
    # Read in lat/long data from dataset
    longs = np.array(ds.groups['navigation_data'].variables['longitude'])
    lats = np.array(ds.groups['navigation_data'].variables['latitude'])

    # Find rows and columns that fit within cropping bounds
    valid_mask = ((lats >= bounds[1]) & (lats <= bounds[3]) &
                  (longs >= bounds[0]) & (longs <= bounds[2]))

    valid_rows, valid_cols = np.where(valid_mask)

    row_min, row_max = valid_rows.min(), valid_rows.max()
    col_min, col_max = valid_cols.min(), valid_cols.max()

    # Crop reflectance data frame and lat/long data frames
    fulldf_cropped = fulldf[row_min:row_max+1, col_min:col_max+1]
    lat_cropped = lats[row_min:row_max+1, col_min:col_max+1]
    lon_cropped = longs[row_min:row_max+1, col_min:col_max+1]

    return fulldf_cropped, lat_cropped, lon_cropped


def read_netcdf(filename, cropto, output=False):
    """Read NASA-formatted netCDF file to a Spectral Data image.

    Parameters
    ----------
    filename : str
        Path of the netCDF file.
    crop : str or list
        Path to a shapefile or list of min/max latitude and longitude for cropping
    output : str (defaults to False, no output)
        Path to output Spectral object as a geotif

    Returns
    -------
    plantcv.plantcv.classes.Spectral_data
        Orthomosaic image data in a Spectral_data class instance
    """
    # Read in file and bounds
    ds = nc.Dataset(filename)
    fulldf, wavelengths = _combine_bands(ds)
    bounds = cropto
    if isinstance(cropto, str):
        bounds = GeoDataFrame.from_file(cropto).total_bounds

    # Crop to bounds
    cropped, lat, lon = _crop_allbands(fulldf, ds, bounds)

    # Calculate affine (important if outputting geotif)
    aff_bounds = rasterio.transform.from_bounds(np.min(lon), np.min(lat), np.max(lon),
                                                np.max(lat), lat.shape[1], lat.shape[0])

    # Make the pseudo_rgb
    id_red = _find_closest_unsorted(array=np.array([float(i) for i in wavelengths]), target=630)
    id_green = _find_closest_unsorted(array=np.array([float(i) for i in wavelengths]), target=540)
    id_blue = _find_closest_unsorted(array=np.array([float(i) for i in wavelengths]), target=480)
    # Stack bands together, BGR since plot_image will convert BGR2RGB automatically
    pseudo_rgb = cv2.merge((cropped[:, :, [id_blue]],
                            cropped[:, :, [id_green]],
                            cropped[:, :, [id_red]]))
    # normalize to [0, 255] if data is not already uint8. If it is uint8 then it should good already.
    if pseudo_rgb.dtype != 'uint8':
        pseudo_rgb = cv2.normalize(pseudo_rgb, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    height, width, depth = cropped.shape
    # Metadata
    metadata = {"driver": "GTiff", "height": height, "width": width,
                "dtype": cropped.dtype, "count": depth,
                "nodata": 0, "crs": rasterio.crs.CRS.from_string("EPSG:4326"),
                "transform": aff_bounds}

    # Make a spectral object
    spectral_array = Spectral_data(array_data=cropped,
                                   max_wavelength=max(wavelengths, key=wavelengths.get),
                                   min_wavelength=min(wavelengths, key=wavelengths.get),
                                   max_value=np.max(cropped), min_value=np.min(cropped),
                                   d_type=cropped.dtype,
                                   wavelength_dict=wavelengths, samples=int(width),
                                   lines=int(height), interleave=None,
                                   wavelength_units="nm", array_type="datacube",
                                   pseudo_rgb=pseudo_rgb, filename=filename,
                                   default_bands=[480, 540, 630],
                                   metadata=metadata)

    # Output to geotif if requested
    if isinstance(output, str):
        out_img = cropped.transpose(2, 0, 1)

        with rasterio.open(output, 'w', **metadata) as dest:
            dest.write(out_img)

    # Add latitude and longitude to metadata
    spectral_array.metadata["latitude"] = lat
    spectral_array.metadata["longitude"] = lon

    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, f"{params.device}_pseudo_rgb.png"))
    return spectral_array
