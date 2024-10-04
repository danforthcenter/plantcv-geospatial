# Save clicked points from Napari or PlantCV-annotate as a geojson points file. 

import geojson
import rasterio
import plantcv.annotate as an
from plantcv.plantcv import fatal_error


def points_to_geojson(img, viewer, output):
    """Use clicks from a Napari or plantcv-annotate viewer to output a geojson shapefile.

    Parameters
    ----------
    img : PlantCV spectral_data class object
        The image used for clicking on points, should be from read_geotif.
    viewer: Napari viewer class object or plantcv-annotate Points class object.
        The viewer used to make the clicks. 
    output : str
        Path to save to shapefile. 
    """
    # Napari output, points must be reversed
    if hasattr(viewer, 'layers'):
        points = [(img.metadata["transform"]*reversed(i)) for i in viewer.layers["Points"].data]
    # Annotate output
    elif hasattr(viewer, 'coords'):
        points = [(img.metadata["transform"]*i) for i in viewer.coords['default']]
    else:
        fatal_error("Viewer class type not recognized. Currently, Napari and PlantCV-annotate viewers supported.")
    features = [geojson.Feature(geometry=geojson.Point((lon, lat))) for lon, lat in points]
    feature_collection = geojson.FeatureCollection(features)
    # Make sure the coordinate system is the same as the original image
    feature_collection['crs'] = {
        "type": "name",
        "properties": {
            "name": rasterio.crs.CRS.to_string(img.metadata["crs"])
        }
    }
    with open(output, 'w') as f:
        geojson.dump(feature_collection, f)