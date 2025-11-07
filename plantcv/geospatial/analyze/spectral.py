# Analyze spectral signature over many regions
from rasterstats import zonal_stats
from plantcv.plantcv import outputs
from plantcv.geospatial._helpers import _plot_bounds_pseudocolored, _gather_ids
import fiona


def spectral_index(img, geojson, percentiles=None, label=None):
    """A function that summarizes pixel intensity values per region for a spectral index
    Inputs:
    img          = Spectral_Data index object of geotif data, used for analysis
    geojson      = Path to the shape file containing the regions for analysis
    percentiles  = list (or other iterable) of percentiles [0-100] scale to calculate (default = None)
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_image = Debug image showing shapes from geojson on input image.

    :param img: [spectral object]
    :param geojson: str
    :return analysis_image: numpy.ndarray
    """
    affine = img.metadata["transform"]

    # Set lable to params.sample_label if no other labels provided
    if label is None:
        # Gather plot IDs from the geojson
        label = _gather_ids(geojson=geojson)
    # set percentiles if missing
    if percentiles is None:
        percentiles = range(0, 101, 25)
    # make percentile strings for zonal_stats
    formatted_pcts = ['median', 'std']
    for _, pct in enumerate(["0", "100", *percentiles]):
        formatted_pcts.append(f"percentile_{pct}")
    formatted_pcts = list(dict.fromkeys(formatted_pcts))
    # Initialize variable for maximum and minimum index values within plots
    plot_lower = []
    plot_upper = []

    # Gather list of IDs
    with fiona.open(geojson, 'r') as shapefile:
        # Add properties to the geojson object, and then should be able to access inside the function called in add_stats
        # Vectorized (efficient) data extraction of spectral signature per sub-region
        stats = zonal_stats(shapefile, img.array_data, affine=affine,
                            stats=formatted_pcts,
                            nodata=-9999)

        for i, id in enumerate(label):
            # Store upper and lower values for each plot
            plot_lower.append(stats[i]['percentile_0'])
            plot_upper.append(stats[i]['percentile_100'])
            # store non-percentile results
            outputs.add_observation(sample=id, variable=f"med_{img.array_type}",
                                    trait=f"Median {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=float(stats[i]['median']), label="none")

            outputs.add_observation(sample=id, variable=f"std_{img.array_type}",
                                    trait=f"Standard deviation {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=stats[i]['std'], label="none")
            # store percentile results
            for pct in formatted_pcts:
                outputs.add_observation(sample=id, variable=f"{pct}_{img.array_type}",
                                        trait=f"{pct}_{img.array_type} value",
                                        method="plantcv.geospatial.analyze.spectral_index", scale="frequency", datatype=float,
                                        value=float(stats[i][pct]), label="none")

    ax = _plot_bounds_pseudocolored(img=img, geojson=geojson, vmin=min(plot_lower), vmax=max(plot_upper),
                                    data_label=img.array_type)

    return ax
