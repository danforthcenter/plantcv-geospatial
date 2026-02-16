# Analyze pixel count over many regions
from plantcv.geospatial._helpers import _gather_ids, _show_geojson
from plantcv.plantcv import outputs, params
from rasterstats import zonal_stats
import numpy as np


def coverage(img, bin_mask, geojson, label=None):
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
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

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
        observation_sample = label + "_" + str(id_lbl)
        # Save out pixel_count
        pixel_count = 0.0
        total = 1.0
        if region_counts[i]["sum"] is not None:
            pixel_count = region_counts[i]["sum"]
        if total_region[i]["sum"] is not None:
            total = total_region[i]["sum"]
        outputs.add_observation(sample=observation_sample, variable="pixel_count", trait="count",
                                method="rasterstats.zonal_stats", scale="pixels", datatype=int,
                                value=pixel_count, label="pixels")
        # Scale and save out coverage in CRS units
        outputs.add_observation(sample=observation_sample, variable="coverage", trait="coverage",
                                method="plantcv-geospatial.analyze.coverage",
                                scale=img.metadata["crs"].linear_units, datatype=float,
                                value=pixel_count * (gsd_x * gsd_y), label="square " + img.metadata["crs"].linear_units)
        # Save out percent coverage
        outputs.add_observation(sample=observation_sample, variable="percent_coverage", trait="percentage",
                                method="rasterstats.zonal_stats", scale="none", datatype=float,
                                value=pixel_count/total, label="none")

    # Save out Ground Sampling Distance
    outputs.add_metadata(term="ground_sampling_distance_x", datatype=float, value=gsd_x)
    outputs.add_metadata(term="ground_sampling_distance_y", datatype=float, value=gsd_y)

    # Plot the GeoTIFF
    plotting_img = _show_geojson(img, geojson, ids=ids)

    return plotting_img
