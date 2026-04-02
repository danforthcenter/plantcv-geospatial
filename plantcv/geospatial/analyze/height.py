# Analyze Digital Surface Model (DSM) over many regions
from plantcv.geospatial._helpers import _gather_ids, _show_geojson
from plantcv.plantcv.classes import Spectral_data
from plantcv.plantcv import outputs, params, fatal_error
from plantcv.plantcv.transform import rescale
from plantcv.plantcv._debug import _debug
from rasterstats import zonal_stats
import numpy as np
import geopandas
import os


def height_percentile(dsm, geojson, lower=25, upper=90, label=None):
    """
    A function that analyzes elevation averages over regions and outputs data.

    Parameters
    ----------
    dsm : plantcv.geospatial.images.DSM object
        Digital surface model data, generally from read_geotif
    geojson : str
        Path to the shape file containing the regions for analysis
    lower : int, optional
        Lower percentile cut off, input as a list formatted  default lower=25
    upper : int, optional
        Upper percentile cut off, input as a list formatted  default upper=90
    label : str, list, optional
        Optional label parameter, modifies the variable name of observations
        recorded (default = pcv.params.sample_label).

    Returns
    -------
    bounds : list
        List of geojson bounds analyzed
    """
    # Set label to params.sample_label if None
    if label is None:
        label = params.sample_label
    # DSM tifs contain just one band of data, so make the array 2D
    dsm_data = dsm[:, :, 0]
    # Cast to float since zonal_stats gives overflow error on uint8 data
    dsm_data = dsm_data.astype(np.float32)

    if dsm.nodata is not None:
        nodata_value = dsm.nodata
    else:
        nodata_value = -999
    # Scale of the data
    scale = dsm.crs.linear_units

    # Vectorize the calculation of mean elevation per region
    lower = "percentile_" + str(lower)
    region_lower_avgs = zonal_stats(geojson, dsm_data,
                                    affine=dsm.transform,
                                    nodata=nodata_value, stats=lower)
    # Vectorize the calculation of mean elevation per region
    upper = "percentile_" + str(upper)
    region_upper_avgs = zonal_stats(geojson, dsm_data,
                                    affine=dsm.transform,
                                    nodata=nodata_value, stats=upper)
    # Gather plot IDs from the geojson
    ids = _gather_ids(geojson=geojson)

    soil_vals = []
    plant_vals = []
    # Save data to outputs
    for i, id_lbl in enumerate(ids):
        # Initialize no data cases
        avg1, avg2, avg = [0.0, 0.0, nodata_value]
        observation_sample = label + "_" + str(id_lbl)
        # Save soil heights
        if region_lower_avgs[i][lower] is not None:
            avg1 = region_lower_avgs[i][lower]
        outputs.add_observation(sample=observation_sample, variable="soil_elevation",
                                trait="dsm_mean_below_" + str(lower),
                                method="plantcv-geospatial.analyze.height",
                                scale=scale, datatype=float,
                                value=avg1, label=scale)
        soil_vals.append(avg1)
        # Save plant heights
        if region_upper_avgs[i][upper] is not None:
            avg2 = region_upper_avgs[i][upper]
        outputs.add_observation(sample=observation_sample, variable="plant_elevation",
                                trait="dsm_mean_above_" + str(upper),
                                method="plantcv-geospatial.analyze.height",
                                scale=scale, datatype=float,
                                value=avg2, label=scale)
        plant_vals.append(avg2)
        if avg1 != 0 and avg2 != 0:
            avg = avg2 - avg1
        outputs.add_observation(sample=observation_sample, variable="plant_height",
                                trait="height",
                                method="plantcv-geospatial.analyze.height",
                                scale=scale, datatype=float,
                                value=avg, label=scale)

    # Min and max height of plots
    min_elevation = min(soil_vals)
    max_elevation = max(plant_vals)

    # Plot the GeoTIFF
    bounds = geopandas.read_file(geojson)

    # Gather representative coordinates for each polygone in the shapefile
    bounds['coords'] = bounds['geometry'].apply(lambda x: x.representative_point().coords[:])
    bounds['coords'] = [coords[0] for coords in bounds['coords']]

    # Plot the GeoTIFF
    plotting_img = _show_geojson(img=dsm, geojson=geojson, ids=ids,
                                 cmap='viridis', vmin=min_elevation, vmax=max_elevation)

    return plotting_img


def height_subtraction(dsm1, dsm0):
    """
    A function that subtracts the height of one DSM from the height of another and outputs a Spectral_data object instance.

    Parameters
    ----------
    dsm1 : plantcv.geospatial.images.DSM object
        Digital surface model data, generally from read_geotif, DSM with plant height
    dsm0 : plantcv.geospatial.images.DSM object
        Digital surface model data, generally from read_geotif, DSM of bare ground

    Returns
    -------
    subtracted_dsm : plantcv.geospatial.images.DSM object
        New DSM image object with dsm1 - dsm0
    """
    # Check the coordinate reference system (CRS) is the same for both of the DSMs
    if dsm1.crs != dsm0.crs:
        fatal_error("The two input DSMs do not have the same coordinate reference system (CRS).")

    # DSM tifs contain just one band of data, so make the array 2D
    dsm1_data = np.squeeze(dsm1)
    dsm0_data = np.squeeze(dsm0)

    # Check for equal arrays
    if np.array_equal(dsm1_data, dsm0_data, equal_nan=True):
        print("Warning: dsm1 and dsm0 have identical array_data, result will be flat.")

    # Check the shapes are equivalent
    if (dsm1_data.shape == dsm0_data.shape) is False:
        fatal_error("Input DSMs do not have same shape, can be changed with PCV 'resize' function.")

    # Perform the subtraction
    final_data = dsm1_data - dsm0_data
    # Create thumb
    final_data.thumb = final_data._create_thumb()

    _debug(visual=final_data.thumb, filename=os.path.join(params.debug_outdir, f"{params.device}_substracted_dsm.png"))
    return final_data
