# Analyze spectral signature over many regions
from rasterstats import zonal_stats
from plantcv.plantcv import outputs, params
from plantcv.plantcv import spectral_index as pcv_spectral
from plantcv.plantcv.classes import Spectral_data
from plantcv.geospatial._helpers import _plot_bounds_pseudocolored, _gather_ids
import fiona
import numpy as np


def _convert_spectral(img, index, distance):
    """Converts a GEO image to a PlantCV spectral object for a particular spectral index
    Parameters:
    ----------
    img : plantcv.geospatial.images.GEO object
        geotif data, generally from read.geotif
    index : str
        Spectral index to convert
    distance : int
        How lenient to be if required wavelengths are not available

    Returns:
    spectral_img : plantcv.plantcv.classes.Spectral_data
        Spectral object with calculated index
    """
    # First, convert GEO image to spectral object
    wavelength_dict = {i : idx for idx, i in enumerate(img.wavelengths)}

    spectral_input = Spectral_data(array_data=img,
                                   max_wavelength=max(img.wavelengths),
                                   min_wavelength=min(img.wavelengths),
                                   max_value=np.nanmax(img), min_value=np.nanmin(img),
                                   d_type=img.dtype,
                                   wavelength_dict=wavelength_dict, samples=img.shape[1],
                                   lines=img.shape[0], interleave=None,
                                   wavelength_units="nm", array_type="datacube",
                                   pseudo_rgb=img.thumb, filename=img.filename,
                                   default_bands=img.default_wavelengths,
                                   metadata={"transform" : img.transform})

    # Calculate index using pcv.spectral_index
    chosen = getattr(pcv_spectral, index)
    return chosen(spectral_input, distance=distance)


def spectral_index(img, geojson, index, percentiles=None, label=None, distance=20):
    """A function that summarizes pixel intensity values per region for a spectral index
    Parameters:
    -----------
    img : plantcv.geospatial.images.GEO object
        geotif data, generally from read_geotif
    geojson : str
        Path to the shape file containing the regions for analysis
    index : str
        Spectral index to calculate
    percentiles : list (or other iterable)
        percentiles [0-100] scale to calculate (default = None)
    label : str
        Optional label parameter, modifies the variable name of
        observations recorded (default = pcv.params.sample_label).
    distance : int
        How lenient to be if required wavelengths are not available.
        Optional (default = 20)

    Returns:
    --------
    analysis_image : numpy.ndarray
        Debug image showing shapes from geojson on input image.
    """
    # Convert input img to spectral reflectance using provided index

    input_img = _convert_spectral(img, index, distance)
    input_img.metadata = {"transform" : img.transform}

    # Set label to params.sample_label if no other labels provided
    if label is None:
        label = params.sample_label
    # Gather plot IDs from the geojson
    shp_labels = _gather_ids(geojson=geojson)
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
        stats = zonal_stats(shapefile, input_img.array_data, affine=img.transform,
                            stats=formatted_pcts,
                            nodata=-9999)

        for i, id in enumerate(shp_labels):
            observation_sample = label + "_" + str(id)
            # Store upper and lower values for each plot
            plot_lower.append(stats[i]['percentile_0'])
            plot_upper.append(stats[i]['percentile_100'])
            # store non-percentile results
            outputs.add_observation(sample=observation_sample, variable=f"med_{input_img.array_type}",
                                    trait=f"Median {input_img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=float(stats[i]['median']), label="none")

            outputs.add_observation(sample=observation_sample, variable=f"std_{input_img.array_type}",
                                    trait=f"Standard deviation {input_img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=stats[i]['std'], label="none")
            # store percentile results
            for pct in formatted_pcts:
                outputs.add_observation(sample=observation_sample, variable=f"{pct}_{input_img.array_type}",
                                        trait=f"{pct}_{input_img.array_type} value",
                                        method="plantcv.geospatial.analyze.spectral_index", scale="frequency", datatype=float,
                                        value=float(stats[i][pct]), label="none")

    ax = _plot_bounds_pseudocolored(img=input_img, geojson=geojson, vmin=min(plot_lower), vmax=max(plot_upper),
                                    data_label=input_img.array_type)

    return ax
