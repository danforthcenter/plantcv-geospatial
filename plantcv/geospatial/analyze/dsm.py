# Analyze Digital Surface Model (DSM) over many regions
from rasterstats import zonal_stats
from plantcv.geospatial._helpers import _gather_ids
from plantcv.plantcv import outputs, params
import numpy as np


def dsm(img, geojson, percentile=[25, 90], label=None):
    """A function that analyzes elevation averages over regions and outputs data.
    Inputs:
    img          = Spectral_Data object of geotif data, used for affine metadata
    geojson      = Path to the shape file containing the regions for analysis
    percentile   = Percetile cut off, input as a list formatted [lower_percentile, upper_percentile],
                   default percentile=[25, 90]
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    :param img: [spectral object]
    :param geojson: str
    :param percentile: list
    :param label: str
    """
    # DSM tifs contain just one band of data, so make the array 2D
    dsm_data = img.array_data[:, :, 0]

    if img.metadata['nodata']:
        nodata_value = img.metadata['nodata']
    else:
        nodata_value = -9999
    # Scale of the data
    scale = img.metadata["crs"].linear_units
    # Filter out no data values, but keep shape by replacing with no-data value
    actual_values = np.where(dsm_data != nodata_value, dsm_data, nodata_value)
    # Vectorize the calculation of mean elevation per region
    lower = "percentile_" + str(percentile[0])
    region_lower_avgs = zonal_stats(geojson, actual_values,
                                    affine=img.metadata["transform"],
                                    nodata=nodata_value, stats=lower)
    # Vectorize the calculation of mean elevation per region
    upper = "percentile_" + str(percentile[1])
    region_upper_avgs = zonal_stats(geojson, actual_values,
                                    affine=img.metadata["transform"],
                                    nodata=nodata_value, stats=upper)
    # Gather plot IDs from the geojson
    ids = _gather_ids(geojson=geojson)

    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    # Save data to outputs
    for i, id_lbl in enumerate(ids):
        # Initialize no data cases
        avg1, avg2, avg = [0.0, 0.0, nodata_value]
        # Save soil heights
        if region_lower_avgs[i][lower] is not None:
            avg1 = region_lower_avgs[i][lower]
        outputs.add_observation(sample=id_lbl, variable="soil_elevation",
                                trait="dsm_mean_below_" + str(percentile[0]),
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg1, label=label)
        # Save plant heights
        if region_upper_avgs[i][upper] is not None:
            avg2 = region_upper_avgs[i][upper]
        outputs.add_observation(sample=id_lbl, variable="plant_elevation",
                                trait="dsm_mean_above_" + str(percentile[1]),
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg2, label=label)
        if avg1 != 0 and avg2 != 0:
            avg = avg2 - avg1
        outputs.add_observation(sample=id_lbl, variable="plant_height",
                                trait="height",
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg, label=label)
