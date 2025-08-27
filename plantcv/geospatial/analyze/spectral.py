# Analyze spectral signature over many regions
from rasterstats import zonal_stats
from plantcv.plantcv import outputs
from _helpers import _plot_bounds_pseudocolored
import numpy as np
import fiona


class Image(np.ndarray):
    """Generic image class that extends the np.ndarray class."""

    # From NumPy documentation
    # Add uri attribute
    def __new__(cls, input_array: np.ndarray, uri: str):
        obj = np.asarray(input_array).view(cls)
        # New attribute uri stores uniform resource identifier of the source file
        obj.uri = uri
        return obj

    def __array_finalize__(self, obj):
        if obj is not None:
            self.uri = getattr(obj, "uri", None)

    def __getitem__(self, key):
        # Enhance the np.ndarray __getitem__ method
        # Slice the array as requested but return an array of the same class
        # Idea from NumPy examples of subclassing:
        return super(Image, self).__getitem__(key)


def spectral_grab(x, props=None):
    print(props)


def spectral_index(img, geojson):
    """A function that summarizes pixel intensity values per region for a spectral index
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

    # If IDs within the geojson
    ids = []
    # Gather list of IDs
    with fiona.open(geojson, 'r') as shapefile:
        ## Add properties to the geojson object, and then should be able to access inside the function called in add_stats
        # Vectorized (efficient) data extraction of spectral signature per sub-region
        stats = zonal_stats(shapefile, img.array_data, affine=affine,
                        stats=['median', 'std', 'percentile_25', 'percentile_50', 'percentile_75'], 
                        #add_stats={'hist': spectral_grab },
                        nodata=-9999)

        for i, row in enumerate(shapefile):
            if 'ID' in row['properties']:
                label = ((row['properties']["ID"]))
            else:
                # If there are no IDs in the geojson then use default labels
                label = ("default_" + str(i))
            ids.append(label)
            # Save data to outputs
            outputs.add_observation(sample=label, variable=f"mean_{img.array_type}", trait=f"Average {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=float(stats[i]['percentile_50']), label="none")

            outputs.add_observation(sample=label, variable=f"med_{img.array_type}", trait=f"Median {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=float(stats[i]['median']), label="none")

            outputs.add_observation(sample=label, variable=f"std_{img.array_type}",
                                    trait=f"Standard deviation {img.array_type} reflectance",
                                    method="plantcv.geospatial.analyze.spectral_index", scale="reflectance", datatype=float,
                                    value=stats[i]['std'], label="none")

            outputs.add_observation(sample=label, variable=f"percentile_25_{img.array_type}",
                                    trait="index frequencies", method="plantcv.geospatial.analyze.spectral_index", scale="frequency",
                                    datatype=float, value=stats[i]['percentile_25'], label="none")

            outputs.add_observation(sample=label, variable=f"percentile_75_{img.array_type}",
                                    trait="index frequencies", method="plantcv.geospatial.analyze.spectral", scale="frequency",
                                    datatype=float, value=stats[i]['percentile_75'], label="none")

    bounds = _plot_bounds_pseudocolored(img=img, geojson=geojson, vmin=img.min_value, vmax=img.max_value)
    return stats
