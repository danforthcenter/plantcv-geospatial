import os
import geojson
import rasterio
import fiona
from plantcv.plantcv.fatal_error import fatal_error


def points(img, source, dest=None, layername="Points"):
    """Convert between Points/Napari.viewer objects and geojson objects/files

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        The image used for clicking on points, or that points from a file should be transformed to match,
        should be from read_geotif.
    source : str, Napari.viewer, or plantcv.annotate.classes.Points object.
        Either a geojson file or a viewer used to click points.
        A geojson file will return a list of coordinates from that geojson.
        A Napari viewer or Points object will save a geojson and return a list of coordinates.
    dest : str
        Path to save to a geojson file to save if source is a Napari viewer or Points object.
        Defaults to None, only required if 'source' is a Napari view or Points object.
    layername : str, optional
        Name of the viewer layer from which to take points.
        Only used if source is a Napari viewer. Defaults to "Points".

    Returns:
    --------
    list or dict, if source is a str then returns a list of X,Y coordinates.
        If source is a Napari.viewer/Points object then a dictionary of geojson data is returned.

    Raises:
    -------
    RunTimeError if source is not an str, Napari.viewer, or plantcv.annotate.classes.Points object.
    """
    if isinstance(source, str):
        # if source is a string then it is path to a geojson file
        return _geojson_to_points(img, filename=source)
    # otherwise, source should be a napari viewer or Points object
    return _points_to_geojson(img, viewer=source, out_path=dest, layername=layername)


def _points_to_geojson(img, viewer, out_path, layername):
    """Use clicks from a Napari or plantcv-annotate viewer to output a geojson shapefile.

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        The image used for clicking on points, should be from read_geotif.
    viewer: Napari.viewer or plantcv.annotate.classes.Points object.
        The viewer used to make the clicks.
    out_path : str
        Path to save to shapefile. Must have "geojson" file extension
    layername : str
        Name of the Napari viewer layer from which to take points.

    Returns:
    --------
    feature_collection : dict, geojson data as a dictionary

    Raises:
    -------
    RunTimeError if out_path is not to a geojson file or viewer is not recognized.
    """
    # Napari output, points must be reversed
    if hasattr(viewer, 'layers'):
        pts = [(img.metadata["transform"]*reversed(i)) for i in viewer.layers[layername].data]
        pts_return = [(float(i[1]), float(i[0])) for i in viewer.layers[layername].data]
    # Annotate output
    elif hasattr(viewer, 'coords'):
        pts = [(img.metadata["transform"]*i) for i in viewer.coords['default']]
        pts_return = viewer.coords['default']
    else:
        fatal_error("Viewer class type not recognized. Currently, Napari and PlantCV-annotate viewers supported.")
    features = [geojson.Feature(geometry=geojson.Point((lon, lat))) for lon, lat in pts]
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

    return pts_return


def _geojson_to_points(img, filename):
    """
    Transform a points-type shapefile or GeoJSON into image pixel coordinates.

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        A spectral image object returned by ``read_geotif``.
    filename : str
        Path to the shapefile or GeoJSON file containing points.

    Returns
    -------
    coord : list of tuple of int
        Pixel coordinates as a list of ``(col, row)`` integer tuples,
        one per point feature in the input file.
    """
    geo_transform = img.metadata["transform"]

    coord = []
    with fiona.open(filename, 'r') as shapefile:
        for row in shapefile:
            if type((row.geometry["coordinates"])) is list:
                pixel_point = ~(geo_transform) * (row.geometry["coordinates"][0])
            if type((row.geometry["coordinates"])) is tuple:
                pixel_point = ~(geo_transform) * (row.geometry["coordinates"])
            rounded = (int(pixel_point[0]), int(pixel_point[1]))
            coord.append(rounded)

    return coord
