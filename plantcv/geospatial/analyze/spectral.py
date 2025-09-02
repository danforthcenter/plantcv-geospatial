# Analyze spectral signature over many regions
from rasterstats import zonal_stats
from plantcv.plantcv import outputs, params
from plantcv.geospatial._helpers import _plot_bounds_pseudocolored, _gather_ids, _set_nodata_term
import fiona


def spectral_index(img, geojson, label=None):
    """A function that summarizes pixel intensity values per region for a spectral index
    Inputs:
    img          = Spectral_Data index object of geotif data, used for analysis
    geojson      = Path to the shape file containing the regions for analysis
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_image = Debug image showing shapes from geojson on input image.

    :param img: [spectral object]
    :param geojson: str
    :return analysis_image: numpy.ndarray
    """
    # Initialize metadata terms
    affine = img.metadata["transform"]
    nodata_value = _set_nodata_term(img)

    # Set lable to params.sample_label if no other labels provided
    if label is None:
        # Gather plot IDs from the geojson
        label = _gather_ids(geojson=geojson)

    # Initialize variable for maximum and minimum index values within plots
    plot_lower = []
    plot_upper = []

    # Gather list of IDs
    with fiona.open(geojson, 'r') as shapefile:
        # Add properties to the geojson object, and then should be able to access inside the function called in add_stats
        # Vectorized (efficient) data extraction of spectral signature per sub-region
        stats = zonal_stats(shapefile, img.array_data, affine=affine,
                            stats=['median', 'std', 'percentile_25', 'percentile_50', 'percentile_75',
                                   'percentile_0', 'percentile_100'],
                            nodata=nodata_value)

        for i, id in enumerate(label):
            # Store upper and lower values for each plot
            plot_lower.append(stats[i]['percentile_0'])
            plot_upper.append(stats[i]['percentile_100'])
            # Save data to outputs
            outputs.add_observation(sample=id, variable=f"min_{img.array_type}",
                                    trait=f"Minumum {img.array_type} value",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=float(stats[i]['percentile_0']), label="none")
            outputs.add_observation(sample=id, variable=f"max_{img.array_type}",
                                    trait=f"Maxiumum {img.array_type} value",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=float(stats[i]['percentile_100']), label="none")
            outputs.add_observation(sample=id, variable=f"mean_{img.array_type}",
                                    trait=f"Average {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=float(stats[i]['percentile_50']), label="none")
            outputs.add_observation(sample=id, variable=f"med_{img.array_type}",
                                    trait=f"Median {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=float(stats[i]['median']), label="none")
            outputs.add_observation(sample=id, variable=f"std_{img.array_type}",
                                    trait=f"Standard deviation {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=stats[i]['std'], label="none")
            outputs.add_observation(sample=id, variable=f"percentile_25_{img.array_type}",
                                    trait=f"percentile_25_{img.array_type}",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="frequency",
                                    datatype=float, value=stats[i]['percentile_25'], label="none")
            outputs.add_observation(sample=id, variable=f"percentile_75_{img.array_type}",
                                    trait=f"percentile_75_{img.array_type}",
                                    method="plantcv.geospatial.analyze.spectral", scale="frequency",
                                    datatype=float, value=stats[i]['percentile_75'], label="none")
    ax = _plot_bounds_pseudocolored(img=img, geojson=geojson, vmin=min(plot_lower), vmax=max(plot_upper),
                                    data_label=img.array_type)

    return ax
