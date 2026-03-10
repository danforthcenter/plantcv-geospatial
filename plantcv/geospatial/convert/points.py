import os
import geojson
import rasterio
import fiona
from plantcv.plantcv.fatal_error import fatal_error


def points(frm, to=None, img=None):
    """Use clicks from a Napari or plantcv-annotate viewer to output a geojson shapefile.

    Parameters
    ----------
    frm : str, Napari.viewer, or plantcv.annotate.classes.Points object.
        Either a geojson file or the viewer used to make the clicks.
        A geojson file will return a list of coordinates from that geojson.
        A Napari viewer or Points object will save and return a geojson object.
    to : str,
        Path to save to a geojson file to save if frm is a Napari viewer or Points object.
        Defaults to None, only required if 'frm' is a Napari view or Points object.
    img : plantcv.plantcv.classes.Spectral_data
        The image used for clicking on points, should be from read_geotif.
        Defaults to None, only required if 'frm' is a Napari view or Points object.

    Raises:
    -------
    RunTimeError if frm is not an str, Napari.viewr, or plantcv.annotate.classes.Points object.
    """
    if isinstance(frm, str):
        # if frm is a string then it is path to a geojson file
        return _geojson_to_points(geojson=frm)
    # otherwise, frm should be a napari viewer or Points object
    return _points_to_geojson(img, viewer=frm, out_path=to)


def _points_to_geojson(img, viewer, out_path):
    """Use clicks frm a Napari or plantcv-annotate viewer to output a geojson shapefile.

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        The image used for clicking on points, should be frm read_geotif.
    viewer: Napari.viewer or plantcv.annotate.classes.Points object.
        The viewer used to make the clicks.
    out_path : str
        Path to save to shapefile. Must have "geojson" file extension

    Raises:
    -------
    RunTimeError if out_path is not to a geojson file or viewer is not recognized.
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
    if os.path.splitext(out_path)[1].lower() != ".geojson":
        out_path = out_path + ".geojson"
        print("File type not supported, writing to " + out_path + " instead")

    with open(out_path, 'w') as f:
        geojson.dump(feature_collection, f)

    return geojson


def _geojson_to_points(geojson):
    """Extract coordinates fr0m geojson

    Parameters
    ----------
    geojson : str, path to geojson file.

    Returns:
    -------
    pts : list, list of X,Y coordinates frm the geometry.coordinates of the geojson file.
    """
    pts = []
    with fiona.open(geojson, "r") as shapefile:
        for row in shapefile:
            pts.append(row['geometry']['coordinates'])
    return pts
