# Analyze pixel count over many regions
from rasterstats import zonal_stats
from plantcv.plantcv import outputs
import fiona 


def pixel_count(img, bin_mask, geojson):
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
mask = bin_mask.astype(float) / 255
affine = img.metadata["transform"]
# Vecctorized (efficient) data extraction of pixel count per sub-region
stats = zonal_stats(geojson,
                    mask,
                    affine=affine,
                    stats="sum")

# If IDs within the geojson
ids = [] 
# Gather list of IDs
with fiona.open(geojson, 'r') as shapefile:
    for row in shapefile:
        temp_list = []
        # Polygon
        if len(row.geometry["coordinates"][0]) > 1:
            square = row.geometry["coordinates"][0][:-1]
            ids.append((row['properties']["ID"]))

# Save data to outputs as custom observation (since using data extraction method not yet integrated into the repo) 
for i, id_lbl in enumerate(ids):
    outputs.add_observation(sample=id_lbl, variable="pixel_count", trait="count",
                            method="rasterstats.zonal_stats", scale="pixels", datatype=int,
                            value=stats[i]["sum"], label="pixels")
