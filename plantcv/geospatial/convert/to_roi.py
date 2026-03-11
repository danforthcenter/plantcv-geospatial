# Transform georeferenced GeoJSON/shapefile points into python coordinates
import os
import numpy as np
from plantcv.geospatial.transform_polygons import transform_polygons
from plantcv.geospatial._helpers import _transform_geojson_crs
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.classes import Objects


def to_roi(img, geojson, radius=None):
    """Takes a points-type shapefile/GeoJSON and transforms circular ROIs,
    saves these out to a new geoJSON file and creates ROI Objects instances

    Parameters:
    -----------
    img : plantcv.plantcv.classes.Spectral_data
        A spectral object from read.geotif.
    geojson : str
        Path to the shape file containing the point or polygon layer.
    radius : optional float
        If provided then points from the geojson will be treated as centers
        of circular ROIs with this radius
        in units matching the coordinate system (CRS) of the image
        e.g. meters

    Returns:
    --------
    rois : list
        List of circular ROIs (plantcv Objects class instances)
    """
    if radius is not None:
        rois = _points_to_circular_rois(img, geojson, radius)
    else :
        rois = _polygon_to_roi(img, geojson)

    return rois


def _points_to_circular_rois(img, geojson, radius):
    """Make circular ROIs from points in a geojson file

    Parameters:
    -----------
    img : plantcv.plantcv.classes.Spectral_data
        A spectral object from read.geotif.
    geojson : str
        Path to the shape file containing the points.    radius : optional float
        If provided then points from the geojson will be treated as centers
        of circular ROIs with this radius
        in units matching the coordinate system (CRS) of the image
        e.g. meters

    Returns:
    --------
    rois : list
        List of circular ROIs (plantcv Objects class instances)
    """
    gdf = _transform_geojson_crs(img=img, geojson=geojson)
    # check that these are points, not polygons
    if "Point" not in gdf.geom_type.unique()[0]:
        fatal_error("Circular ROIs can only be specified with points layers, geojson file is geom_type '" +
                    ", ".join(gdf.geom_type.unique()) + "'")

    gdf['geometry'] = gdf.geometry.buffer(radius)

    buffered_geojson = os.path.splitext(geojson)[0] + '_circles.geojson'
    gdf.to_file(buffered_geojson, driver='GeoJSON')

    geo_polygons = transform_polygons(img=img, geojson=buffered_geojson)
    rois = Objects()
    for polygon in geo_polygons:
        rois.append(contour=[np.array(polygon)], h=[])

    return rois


def _polygon_to_roi(img, geojson):
    """Make circular ROIs from points in a geojson file

    Parameters:
    -----------
    img : plantcv.plantcv.classes.Spectral_data
        A spectral object from read.geotif.
    geojson : str
        Path to the shape file containing the points.

    Returns:
    --------
    rois : list
        List of polygon ROIs (plantcv Objects class instances)
    """
    gdf = _transform_geojson_crs(img=img, geojson=geojson)
    # check that these are polygons, not points
    if "Polygon" not in gdf.geom_type.unique()[0]:
        fatal_error("Polygon ROIs can only be specified with polygon layers, geojson file is geom_type '" +
                    ", ".join(gdf.geom_type.unique()) + "'")

    buffered_geojson = os.path.splitext(geojson)[0] + '_polygons.geojson'
    gdf.to_file(buffered_geojson, driver='GeoJSON')

    geo_polygons = transform_polygons(img=img, geojson=buffered_geojson)

    rois = Objects()
    for polygon in geo_polygons:
        rois.append(contour=[np.array(polygon)], h=[])

    return rois
