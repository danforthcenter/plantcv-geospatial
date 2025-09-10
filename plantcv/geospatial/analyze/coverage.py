# Analyze pixel count over many regions
from plantcv.geospatial._helpers import _gather_ids
from plantcv.plantcv import outputs, params
from rasterio.plot import plotting_extent
from rasterstats import zonal_stats
from matplotlib import pyplot as plt
import geopandas
import numpy as np
import os
import cv2


def coverage(img, bin_mask, geojson):
    """A function that analyzes pixel coverage in a binary mask and outputs data.
    Inputs:
    img          = Spectral_Data object of geotif data, used for affine metadata
    bin_mask     = Binary mask of objects (32-bit).
    geojson      = Path to the shape file containing the regions for analysis

    Returns:
    analysis_image = Debug image showing shapes from geojson on input image.

    :param img: [spectral object]
    :param bin_mask: numpy.ndarray
    :param geojson: str
    :return analysis_image: numpy.ndarray
    """
    # zonal_stats "sum" gives the sum of pixel values, so change from [0,255] to [0,1]
    bin_mask = np.where(bin_mask > 0, 1, 0)
    all_ones = np.ones(bin_mask.shape[:2])
    affine = img.metadata["transform"]

    # Calculate GSD in the x and y directions
    gsd_x = abs(affine[0])
    gsd_y = abs(affine[4])

    # Vectorized (efficient) data extraction of pixel count per sub-region
    region_counts = zonal_stats(geojson, bin_mask, affine=affine, stats="sum")

    total_region = zonal_stats(geojson, all_ones, affine=affine, stats="sum")

    # Gather list of IDs
    ids = _gather_ids(geojson=geojson)

    # Save data to outputs
    for i, id_lbl in enumerate(ids):
        # Save out pixel_count
        pixel_count = 0.0
        total = 1.0
        if region_counts[i]["sum"] is not None:
            pixel_count = region_counts[i]["sum"]
        if total_region[i]["sum"] is not None:
            total = total_region[i]["sum"]
        outputs.add_observation(sample=id_lbl, variable="pixel_count", trait="count",
                                method="rasterstats.zonal_stats", scale="pixels", datatype=int,
                                value=pixel_count, label="pixels")
        # Scale and save out coverage in CRS units
        outputs.add_observation(sample=id_lbl, variable="coverage", trait="coverage",
                                method="plantcv-geospatial.analyze.coverage",
                                scale=img.metadata["crs"].linear_units, datatype=float,
                                value=pixel_count * (gsd_x * gsd_y), label="square " + img.metadata["crs"].linear_units)
        # Save out percent coverage
        outputs.add_observation(sample=id_lbl, variable="percent_coverage", trait="percentage",
                                method="rasterstats.zonal_stats", scale="none", datatype=float,
                                value=pixel_count/total, label="none")

    # Save out Ground Sampling Distance
    outputs.add_metadata(term="ground_sampling_distance_x", datatype=float, value=gsd_x)
    outputs.add_metadata(term="ground_sampling_distance_y", datatype=float, value=gsd_y)

    bounds = geopandas.read_file(geojson)

    # Plot the GeoTIFF
    # Make a flipped image for graphing
    flipped = cv2.merge((img.pseudo_rgb[:, :, [2]],
                         img.pseudo_rgb[:, :, [1]],
                         img.pseudo_rgb[:, :, [0]]))

    _, ax = plt.subplots(figsize=(10, 10))
    fig_extent = plotting_extent(img.array_data[:, :, :3],
                                 img.metadata['transform'])
    ax.imshow(flipped, extent=fig_extent)
    # Plot the shapefile
    bounds.boundary.plot(ax=ax, color="red")
    # Add labels to vector features
    for idx, row in bounds.iterrows():
        plt.text(row.geometry.centroid.x,
                 row.geometry.centroid.y,
                 ids[idx], fontsize=5,
                 c="m")
    # Set plot title and labels
    plt.title("Shapefile on GeoTIFF")
    # Store the plot
    plotting_img = plt.gcf()

    # Print or plot if debug is turned on
    if params.debug is not None:
        if params.debug == 'print':
            plt.savefig(os.path.join(params.debug_outdir, str(
                params.device) + '_analyze_coverage.png'), dpi=params.dpi)
            plt.close()
        elif params.debug == 'plot':
            # Use non-blocking mode in case the function is run more than once
            plt.show(block=False)
    else:
        plt.close()

    return plotting_img
