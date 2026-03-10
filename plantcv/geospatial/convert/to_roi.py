# Transform georeferenced GeoJSON/shapefile points into python coordinates
import os
import numpy as np
from plantcv.geospatial.transform_polygons import transform_polygons
from plantcv.geospatial._helpers import _transform_geojson_crs
from plantcv.plantcv import Objects


def to_roi(img, geojson, radius):
    """Takes a points-type shapefile/GeoJSON and transforms circular ROIs,
    saves these out to a new geoJSON file and creates ROI Objects instances

    Parameters:
    -----------
    img : plantcv.plantcv.classes.Spectral_data
        A spectral object from read_geotif.
    geojson : str
        Path to the shape file containing the points.
    radius : float
        Radius of circular ROIs to get created,
        in units matching the coordinate system (CRS) of the image
        e.g. meters

    Returns:
    --------
    rois : list
        List of circular ROIs (plantcv Objects class instances)
    """
    gdf = _transform_geojson_crs(img=img, geojson=geojson)

    gdf['geometry'] = gdf.geometry.buffer(radius)

    buffered_geojson = os.path.splitext(geojson)[0] + '_circles.geojson'
    gdf.to_file(buffered_geojson, driver='GeoJSON')

    geo_polygons = transform_polygons(img=img, geojson=buffered_geojson)

    return _points2roi(geo_polygons)


def _points2roi(polygon_list):
    """Helper that takes ROI contour coordinates and populates
    a plantcv Objects class instance

    Parameters:
    -----------
    polygon_list : list
        Pixel coordinates as a nested list of polygons as returned from transform_polygons

    Returns:
    --------
    rois : plantcv.Objects instance
        grouped contours list
    """
    rois = Objects()
    for polygon in polygon_list:
        rois.append(contour=[np.array(polygon)], h=[])

    return rois
