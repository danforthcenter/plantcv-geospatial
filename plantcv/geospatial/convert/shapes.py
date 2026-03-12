import os
import geojson
import rasterio
from shapely.geometry import Polygon, mapping
from plantcv.geospatial.convert.points import _geojson_to_points


def shapes(source, dest=None, img=None, shapetype="polygon", layername="Shapes"):
    """Use clicks from a Napari or plantcv-annotate viewer to output a geojson shapefile.

    Parameters:
    -----------
    source : str, Napari.viewer
        Either a geojson file or the viewer used to make the clicks.
        A geojson file will return a list of coordinates from that geojson.
        A Napari viewer will save and return a geojson object.
    dest : str,
        Path to save to a geojson file to save if source is a Napari viewer or Points object.
        Defaults to None, only required if 'source' is a Napari view or Points object.
    img : plantcv.plantcv.classes.Spectral_data
        The image used for clicking on points, should be from read_geotif.
        Defaults to None, only required if 'source' is a Napari view or Points object.
    shapetype: str, optional
        Geometry type from Napari viewer shape layer desired for geojson output, defaults to "polygon."
    shapename: str, optional
        Name of shapes layer, defaults to "Shapes."

    Returns:
    --------
    list or dict, if source is a str then returns a list of X,Y coordinates.
        If source is a Napari.viewer then a dictionary of geojson data is returned.
    """
    if isinstance(source, str):
        # a shape here is just a collection of points, so we use the points helper
        return _geojson_to_points(filename=source)
    # otherwise source should be a napari viewer
    return _shape_to_geojson(img=img, viewer=source, out_path=dest, shapetype=shapetype, layername=layername)


def _shape_to_geojson(img, viewer, out_path, shapetype="polygon", layername="Shapes"):
    """Use shapes from a Napari to output a geojson shapefile.

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        The image used for making the Napari viewer, should be from read_geotif.
    viewer: Napari.viewer
        The viewer used to draw the shapes.
    out_path : str
        Path to save to shapefile. Must have "geojson" file extension.
    shapetype: str, optional
        Geometry type from Napari viewer shape layer desired for geojson output, defaults to "polygon."
    shapename: str, optional
        Name of shapes layer, defaults to "Shapes".

    Returns:
    --------
    feature_collection : dict, geojson data as a dictionary
    """
    features = []
    for i in viewer.layers[layername].data:
        shape = []
        for j in i:
            shape.append((img.metadata["transform"]*(j[1], j[0])))
        features.append(shape)

    polygon_list = []
    for i, _ in enumerate(features):
        shape_type = viewer.layers[layername].shape_type[i]
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
    if os.path.splitext(out_path)[1].lower() != ".geojson":
        out_path = out_path + ".geojson"
        print("File type not supported, writing to " + out_path + " instead")

    with open(out_path, 'w') as f:
        geojson.dump(feature_collection, f)

    return feature_collection
