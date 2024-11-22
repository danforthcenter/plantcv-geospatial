# Analyze pixel count over many regions
from rasterstats import zonal_stats
from plantcv.plantcv import outputs
import numpy as np
import fiona


def coverage(img, bin_mask, geojson):
    """A function that analyzes the shape and size of objects and outputs data.

    Inputs:
    img          = Spectral_Data object of geotif data, used for affine metadata
    bin_mask     = Binary mask of objects (32-bit).
    geojson      = Path to the shape file containing the regions for analysis

    Returns:
    analysis_image = Diagnostic image showing measurements.

    :param img: [spectral object]
    :param bin_mask: numpy.ndarray
    :param geojson: str
    :return analysis_image: numpy.ndarray
    """

    # sum gives the sum of pixel values, so change from [0,255] to [0,1]
    bin_mask = bin_mask.astype(float) / 255  # set values to one a safer way like np.where
    all_ones = np.ones(bin_mask.shape[:2])
    affine = img.metadata["transform"]

    # Calculate GSD in the x and y directions
    gsd_x = abs(affine[0])
    gsd_y = abs(affine[4])
    # Vectorized (efficient) data extraction of pixel count per sub-region
    region_counts = zonal_stats(geojson, bin_mask, affine=affine, stats="sum")

    total_region = zonal_stats(geojson, all_ones, affine=affine, stats="sum")

    # If IDs within the geojson
    ids = []
    # Gather list of IDs
    with fiona.open(geojson, 'r') as shapefile:
        for i, row in enumerate(shapefile):
            if 'ID' in row['properties']:
                ids.append((row['properties']["ID"]))
            else:
                # If there are no IDs in the geojson then use default labels
                ids.append("default_" + str(i))

    # Save data to outputs
    for i, id_lbl in enumerate(ids):
        # Save out pixel_count
        outputs.add_observation(sample=id_lbl, variable="pixel_count", trait="count",
                                method="rasterstats.zonal_stats", scale="pixels", datatype=int,
                                value=region_counts[i]["sum"], label="pixels")
        # Scale and save out coverage in CRS units
        outputs.add_observation(sample=id_lbl, variable="coverage", trait="coverage",
                                method="plantcv-geospatial.analyze.coverage",
                                scale=img.metadata["crs"].linear_units, datatype=float,
                                value=region_counts[i]["sum"]/gsd_x, label=img.metadata["crs"].linear_units)
        # Save out Ground Sampling Distance(s)
        outputs.add_observation(sample=id_lbl, variable="ground_sampling_distance", trait="gsd",
                                method="rasterio", scale=img.metadata["crs"].linear_units, datatype=tuple,
                                value=(gsd_x, gsd_y), label=["gsd_x", "gsd_y"])
        # Save out percent coverage 
        outputs.add_observation(sample=id_lbl, variable="percent_coverage", trait="percentage",
                                method="rasterstats.zonal_stats", scale="none", datatype=float,
                                value=region_counts[i]["sum"]/total_region[i]["sum"], label="none")
