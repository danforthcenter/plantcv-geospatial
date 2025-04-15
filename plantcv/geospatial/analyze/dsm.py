# Analyze Digital Surface Model (DSM) over many regions
from plantcv.geospatial._helpers import _gather_ids
from plantcv.plantcv import outputs, params
from rasterio.plot import plotting_extent
from matplotlib import pyplot as plt
from rasterstats import zonal_stats
import numpy as np
import geopandas
import cv2


def height_percentile(dsm, geojson, percentile=[25, 90], label=None):
    """A function that analyzes elevation averages over regions and outputs data.
    Inputs:
    dsm          = Spectral_Data object of geotif data, used for affine metadata
    geojson      = Path to the shape file containing the regions for analysis
    percentile   = Percetile cut off, input as a list formatted [lower_percentile, upper_percentile],
                   default percentile=[25, 90]
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    :param dsm: [spectral object]
    :param geojson: str
    :param percentile: list
    :param label: str
    """
    # DSM tifs contain just one band of data, so make the array 2D
    dsm_data = dsm.array_data[:, :, 0]

    if dsm.metadata['nodata']:
        nodata_value = dsm.metadata['nodata']
    else:
        nodata_value = -9999
    # Scale of the data
    scale = dsm.metadata["crs"].linear_units
    # Filter out no data values, but keep shape by replacing with no-data value
    actual_values = np.where(dsm_data != nodata_value, dsm_data, nodata_value)
    # Vectorize the calculation of mean elevation per region
    lower = "percentile_" + str(percentile[0])
    region_lower_avgs = zonal_stats(geojson, actual_values,
                                    affine=dsm.metadata["transform"],
                                    nodata=nodata_value, stats=lower)
    # Vectorize the calculation of mean elevation per region
    upper = "percentile_" + str(percentile[1])
    region_upper_avgs = zonal_stats(geojson, actual_values,
                                    affine=dsm.metadata["transform"],
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
                                trait="dsm_percentile_" + str(percentile[0]),
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg1, label=label)
        # Save plant heights
        if region_upper_avgs[i][upper] is not None:
            avg2 = region_upper_avgs[i][upper]
        outputs.add_observation(sample=id_lbl, variable="plot_elevation",
                                trait="dsm_percentile_" + str(percentile[1]),
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg2, label=label)
        if avg1 != 0 and avg2 != 0:
            avg = avg2 - avg1
        outputs.add_observation(sample=id_lbl, variable="plot_height",
                                trait="height",
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg, label=label)
        
    # Plot the GeoTIFF
    bounds = geopandas.read_file(geojson)
    # Make a flipped image for graphing
    flipped = cv2.merge((dsm.pseudo_rgb[:, :, [2]],
                         dsm.pseudo_rgb[:, :, [1]],
                         dsm.pseudo_rgb[:, :, [0]]))

    _, ax = plt.subplots(figsize=(10, 10))
    fig_extent = plotting_extent(dsm.array_data[:, :, :3],
                                 dsm.metadata['transform'])
    ax.imshow(flipped, extent=fig_extent)
    # Plot the shapefile
    bounds.boundary.plot(ax=ax, color="red")
    # Set plot title and labels
    plt.title("Shapefile on GeoTIFF")
    # Store the plot
    plotting_img = plt.gcf()
