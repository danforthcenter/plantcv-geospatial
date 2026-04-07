# Read NASA-formatted netCDF files to Spectral Image data

import netCDF4 as nc
import numpy as np
import cv2
import os
import rasterio
from plantcv.plantcv import params, transform
from plantcv.plantcv._debug import _debug
from plantcv.geospatial.images import GEO, DSM
from geopandas import GeoDataFrame


def _read_to_class(depth, img, filename, wavelengths, crs, transform, nodata, cutoff):
    """Read to either a GEO or DSM class based on depth

    Parameters:
    -----------
    depth       = int, depth of img
    img         = numpy.ndarray, image data
    filename    = str, filename
    wavelengths = list, list of wavelengths
    crs         = rasterio.crs.CRS object, coordinate reference system
    transform   = rasterio transformation
    cutoff      = float, cutoff for a grayscale image (DSM)
    
    Returns:
    --------
    obj         = GEO or DSM object
    """
    if depth > 1:
        # Make a GEO instance before calculating a pseudo-rgb
        obj = GEO(input_array=img,
                  filename=filename,
                  wavelengths=wavelengths,
                  default_wavelengths=[650, 560, 480],
                  crs=crs,
                  transform=transform,
                  nodata=nodata
                  )
    else:
        obj = DSM(input_array=img,
                  filename=filename,
                  crs=crs,
                  transform=transform,
                  nodata=nodata,
                  cutoff=cutoff
                  )
    return obj


def _combine_bands(ds):
    """Combine bands from individual netCDF variables.

    Parameters
    ----------
    ds : netCDF dataset read in with netCDF4 package

    Returns
    -------
    fullmat : numpy.ndarray
        Array of combined data from all bands
    wavelengths : list
        List of wavelengths
    """
    # Pull all available bands using name of variable
    params_set = params.debug
    params.debug = None
    bands = []
    wavelengths = []
    # Currently only supporting NASA formatting where all bands are in
    # the `geospatial_data` variables, could be extended to have more
    # modes if other reasonable formats are popularized.
    for idx, i in enumerate(ds.groups['geophysical_data'].variables):
        if i[0:4] == "rhos":
            bands.append(i)
            wavelengths.append(idx)
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
    fulldf : numpy.ndarray
        Combined data frame of all bands
    ds : netCDF dataset read in with netCDF4 package
    bounds : list
        List of min/max latitude and longitude to crop to

    Returns
    -------
    fulldf_cropped : numpy.ndarray
        Combine bands data frame cropped to bounds
    lat_cropped : numpy.ndarray
        Cropped latitude data frame
    lon_cropped : numpy.ndarray
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


def netcdf(filename, cropto, output=False, cutoff=None):
    """Read NASA-formatted netCDF file to a Spectral Data image.

    Parameters
    ----------
    filename : str
        Path of the netCDF file.
    crop : str or list
        Path to a shapefile or list of min/max latitude and longitude for cropping.
    output : str (optional)
        Path to output Spectral object as a geotif (defaults to False, no output).
    cutoff: float, optional
        Percentile above which to remove points (only used for grayscale
        images). Default is None.

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

    height, width, depth = cropped.shape

    # Make an Image object based on dimensions
    obj = _read_to_class(depth, cropped, filename, wavelengths,
                         rasterio.crs.CRS.from_string("EPSG:4326"), aff_bounds, 0, cutoff)

    # Output to geotif if requested
    if isinstance(output, str):
        out_img = cropped.transpose(2, 0, 1)

        with rasterio.open(output, 'w', height=height, width=width, count=len(wavelengths), dtype=cropped.dtype) as dest:
            dest.write(out_img)

    _debug(visual=obj.thumb, filename=os.path.join(params.debug_outdir, f"{params.device}_pseudo_rgb.png"))
    return obj
