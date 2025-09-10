# Save shapes from a Napari shapes layer as a geojson polygon file.

import geojson
import rasterio
from shapely.geometry import Polygon, mapping
from plantcv.plantcv import fatal_error


def shapes_to_geojson(img, viewer, out_path, shapetype="polygon", shapename="Shapes"):
    """Use shapes from a Napari to output a geojson shapefile.

    Parameters
    ----------
    img : PlantCV spectral_data class object
        The image used for making the Napari viewer, should be from read_geotif.
    viewer: Napari viewer class object.
        The viewer used to draw the shapes.
    out_path : str
        Path to save to shapefile. Must have "geojson" file extension.
    shapetype: str
        Geometry type from Napari viewer shape layer desired for geojson output.
    shapename: str
        Name of shapes layer, defaults to "Shapes"
    """
    features = []
    for i in viewer.layers[shapename].data:
        shape = []
        for j in i:
            shape.append((img.metadata["transform"]*(j[1], j[0])))
        features.append(shape)

    polygon_list = []
    for i, _ in enumerate(features):
        shape_type = viewer.layers[shapename].shape_type[i]
        if shape_type == shapetype:
            polygon = Polygon(features[i])
            geojson_feature = {
                "type": "Feature",
                "geometry": mapping(polygon),
                "properties": {}
            }
            polygon_list.append(geojson_feature)

    feature_collection = geojson.FeatureCollection(polygon_list)
    feature_collection['crs'] = {
        "type": "name",
        "properties": {
            "name": rasterio.crs.CRS.to_string(img.metadata["crs"])
        }
    }

    if ".geojson" in out_path:
        with open(out_path, 'w') as f:
            geojson.dump(feature_collection, f)
    else:
        fatal_error("File type not supported.")
