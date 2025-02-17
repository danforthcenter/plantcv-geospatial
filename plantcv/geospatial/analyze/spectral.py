# Analyze spectral signature over many regions
from rasterstats import zonal_stats
from plantcv.plantcv import outputs, params
from plantcv.plantcv.visualize import pseudocolor
from matplotlib import pyplot as plt
from rasterio.plot import plotting_extent
import geopandas
import fiona
import os


def spectral(img, geojson):
    """A function that analyzes pixel intensity values for a spectral index
    Inputs:
    img          = Spectral_Data index object of geotif data, used for analysis
    geojson      = Path to the shape file containing the regions for analysis

    Returns:
    analysis_image = Debug image showing shapes from geojson on input image.

    :param img: [spectral object]
    :param geojson: str
    :return analysis_image: numpy.ndarray
    """
    bin_label = []
    affine = img.metadata["transform"]

    # Vectorized (efficient) data extraction of spectral signature per sub-region
    stats = zonal_stats(geojson, img.array_data, affine=affine,
                        stats=['mean', 'median', 'std', 'count'], nodata=-9999)

    # If IDs within the geojson
    ids = []
    # Gather list of IDs
    with fiona.open(geojson, 'r') as shapefile:
        for i, row in enumerate(shapefile):
            if 'ID' in row['properties']:
                label = ((row['properties']["ID"]))
            else:
                # If there are no IDs in the geojson then use default labels
                label = ("default_" + str(i))
            ids.append(label)
            # Save data to outputs
            outputs.add_observation(sample=label, variable=f"mean_{img.array_type}", trait=f"Average {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral", scale="reflectance", datatype=float,
                                    value=float(stats[i]['mean']), label="none")

            outputs.add_observation(sample=label, variable=f"med_{img.array_type}", trait=f"Median {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral", scale="reflectance", datatype=float,
                                    value=float(stats[i]['median']), label="none")

            outputs.add_observation(sample=label, variable=f"std_{img.array_type}",
                                    trait=f"Standard deviation {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral", scale="reflectance", datatype=float,
                                    value=stats[i]['std'], label="none")

            outputs.add_observation(sample=label, variable=f"index_frequencies_{img.array_type}",
                                    trait="index frequencies", method="plantcv.geospatial.analyze.spectral", scale="frequency",
                                    datatype=list, value=stats[i]['count'], label=bin_label)

    bounds = geopandas.read_file(geojson)

    # Plot the GeoTIFF
    # Make a flipped image for graphing
    vis = pseudocolor(gray_img=img.array_data, min_value=img.array_data.min, max_value=img.array_data.max)

    _, ax = plt.subplots(figsize=(10, 10))
    fig_extent = plotting_extent(img.array_data[:, :, :3],
                                 img.metadata['transform'])
    ax.imshow(vis, extent=fig_extent)
    # Plot the shapefile
    bounds.boundary.plot(ax=ax, color="red")
    # Set plot title and labels
    plt.title("Shapefile on GeoTIFF")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
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
