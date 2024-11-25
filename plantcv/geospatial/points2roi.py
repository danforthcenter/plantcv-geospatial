# Transform georeferenced GeoJSON/shapefile points into python coordinates
import geopandas
from plantcv.geospatial.transform_polygons import transform_polygons
from plantcv.plantcv import Objects


def points2roi_circle(img, geojson, radius):
    """Takes a points-type shapefile/GeoJSON and transforms circular ROIs,
    saves these out to a new geoJSON file and creates ROI Objects instances
    Inputs:
    img:        A spectral object from read_geotif.
    geojson:    Path to the shape file containing the points.
    radius:     Radius of circular ROIs to get created,
                in units matching the coordinate system (CRS) of the image
                e.g. meters

    Returns:
    rois:       List of circular ROIs (plantcv Objects class instances)

    :param img: [spectral object]
    :param geojson: str
    :param radius: float
    :return rois: list
    """
    gdf = geopandas.read_file(geojson)

    img_crs = img.metadata['crs']

    #check if CRS of spectral objecte and geojson are meter-based, if not then convert into metere-based coordinate
    if not gdf.crs.is_projected:
       gdf = gdf.to_crs(epsg=32615)
        
    if not img_crs.is_projected:
       img.metadata['crs'] = "EPSG:32615" 
         
    gdf['geometry'] = gdf.geometry.buffer(radius)

    buffered_geojson = geojson + '_circles.geojson'
    gdf.to_file(buffered_geojson, driver='GeoJSON')

    geo_rois = transform_polygons(img=img, geojson=buffered_geojson)

    return _points2roi(geo_rois)


def _points2roi(roi_list):
    """
    Helper that takes ROI contour coordinates and populates a plantcv Objects class instance

    Inputs:
    roi_list  = List of ROI contours from georeferenced origin

    Returns:
    group    = grouped contours list

    :param roi_list: list
    :return rois: plantcv.plantcv.classes.Objects
    """
    rois = Objects()
    for roi in roi_list:
        rois.append(contour=roi, h=[])

    return rois