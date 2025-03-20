# Analyze Digital Surface Model (DSM) over many regions
from rasterstats import zonal_stats
from plantcv.geospatial._helpers import _gather_ids
from plantcv.plantcv import outputs
import numpy as np


def dsm(img, geojson, percentile=[50, 80]):
    """A function that analyzes elevation averages over regions and outputs data.
    Inputs:
    img          = Spectral_Data object of geotif data, used for affine metadata
    geojson      = Path to the shape file containing the regions for analysis
    percentile   = Percetile cut off, formatted [lower_percentile, upper_percentile],
                   default percentile=[50, 80]

    Returns:
    analysis_image = Debug image showing shapes from geojson on input image.

    :param img: [spectral object]
    :param geojson: str
    :param percentile: list
    :return analysis_image: numpy.ndarray
    """
    dsm_data = img.array_data
    # Set no data value if there is one
    if img.metadata['nodata']:
        nodata_value = img.metadata['nodata']
    else:
        nodata_value = -9999
    # Scale of the data 
    scale = img.metadata["crs"].linear_units
    # Filter out no data values
    actual_values = dsm_data[dsm_data != nodata_value]
    # Calculate the 50th percentile (median)
    percentile = np.percentile(actual_values, percentile[0])
    # Filter values below the lower_percentile and calculate the average
    below_percentile_values = actual_values[actual_values < percentile[0]]
    # Filter values above the Upper_percentile and calculate the average
    above_percentile_values = actual_values[actual_values > percentile[1]]
    # Vectorize the calculation of mean elevation per region
    region_lower_avgs = zonal_stats(geojson, below_percentile_values,
                                    affine=img.metadata["transform"], stats="mean")
    # Vectorize the calculation of mean elevation per region
    region_upper_avgs = zonal_stats(geojson, above_percentile_values,
                                    affine=img.metadata["transform"], stats="mean")
    # Gather plot IDs from the geojson
    ids = _gather_ids(geojson=geojson)

    # Save data to outputs
    for i, id_lbl in enumerate(ids):
        # Initialize no data cases
        avg1, avg2, avg = [0.0, 0.0, nodata_value]
        # Save soil heights
        if region_lower_avgs[i]["mean"] is not None:
            avg1 = region_lower_avgs[i]["mean"]
        outputs.add_observation(sample=id_lbl, variable="soil_elevation",
                                trait="dsm_mean_below_" + str(percentile),
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg1, label="soil_elevation")
        # Save plant heights
        if region_upper_avgs[i]["mean"] is not None:
            avg2 = region_upper_avgs[i]["mean"]
        outputs.add_observation(sample=id_lbl, variable="plant_elevation",
                                trait="dsm_mean_above_" + str(percentile),
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg2, label="plant_elevation")
        if avg1 != 0 and avg2 != 0:
            avg = avg2 - avg1
        outputs.add_observation(sample=id_lbl, variable="plant_height",
                                trait="height",
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg, label="plant_height")
    
