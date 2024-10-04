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
                in units matching the coordinate system of the image

    Returns:
    rois:       List of circular ROIs (plantcv Objects class instances)

    :param img: [spectral object]
    :param geojson: str
    :param radius: float
    :return rois: list
    """
    gdf = geopandas.read_file(geojson)

    # Specify the desired diameter (in the same units as the CRS, e.g., meters)
    radius = radius  # Half the diameter to use as buffer radius

    # Generate a circle (buffer) around each point
    gdf['geometry'] = gdf.geometry.buffer(radius)

    # Save the resulting circles as a GeoJSON file
    gdf.to_file(geojson + '_circles.geojson', driver='GeoJSON')

    geo_rois = transform_polygons(img=img, geojson=geojson + '_circles.geojson')
    rois = Objects()
    for roi in geo_rois:
        rois.append(contour=roi, h=[])

    return rois
