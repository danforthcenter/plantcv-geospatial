import os
import geojson
import rasterio
from shapely.geometry import Polygon, mapping
from plantcv.plantcv.fatal_error import fatal_error


def shapes(frm, to=None, outpath=None):
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
    
