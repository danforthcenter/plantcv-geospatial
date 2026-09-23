# Transform georeferenced GeoJSON/shapefile points into python coordinates
import numpy as np
from plantcv.geospatial._helpers import _to_gdf, _gdf_to_pixel_polygons
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.classes import Objects
from plantcv.plantcv.roi.roi_methods import _draw_roi


def to_roi(img, source, radius=None, layername="Shapes"):
    """Takes a points- or polygon-type shapefile/GeoJSON and transforms to ROIs,
    and creates ROI Objects instances. If points, saves circular ROIs out to a new geoJSON file.

    Parameters:
    -----------
    img : plantcv.geospatial.images.GEO object
        A GEO image object returned by ``read_geotif``.
    source : str, InteractiveShapes, or Napari Viewer
        This should provide points/polygons.
        An str will be treated as a filepath to a geojson file.
        An InteractiveShapes instance will have the viewer used.
        A Napari Viewer will have the specified layername used to make ROIs.
    radius : optional float
        If provided, then points from the geojson will be treated as centers
        of circular ROIs with this radius
        in units matching the coordinate system (CRS) of the image.
        This should only be used with Point/MultiPoint layers.

    Returns:
    --------
    rois : list
        List of circular ROIs (plantcv Objects class instances)
    """
    gdf = _to_gdf(img, source, layername)
    geom_types = set(gdf.geom_type)
    if radius is not None:
        if not geom_types <= {"Point", "MultiPoint"}:
            fatal_error("A radius was specified but can only be used with Point and MultiPoint geometries. " +
                        "Source contains '" + ", ".join(gdf.geom_type.unique()) + "'"
                        )
        gdf = gdf.assign(geometry=gdf.geometry.buffer(radius))
    elif not geom_types <= {"Polygon", "MultiPolygon"}:
        fatal_error("Non-polygon ROIs require a radius. Source is geom_type '" +
                    ", ".join(gdf.geom_type.unique()) + "'")

    rois = Objects()
    for polygon in _gdf_to_pixel_polygons(img, gdf):
        rois.append(contour=[np.array(polygon)], h=[])
    _draw_roi(img=img.thumb, roi_contour=rois)
    return rois
