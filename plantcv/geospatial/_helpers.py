# PlantCV-geospatial helper functions
import geopandas


def _transform_geojson_crs(img, geojson):
    """
    Helper function for opening and transforming Coordinate System
    of a geojson/shapefile

    Keyword inputs:
    Inputs:
    img:        A spectral object from read_geotif.
    geojson:    Path to the shapefile.

    :param img: [spectral object]
    :return geojson: str
    :return gdf: geopandas
    """
    gdf = geopandas.read_file(geojson)

    img_crs = img.metadata['crs']

    # Check spectral object and geojson have the same CRS, if not then convert
    if not gdf.crs == img_crs:
        gdf = gdf.to_crs(crs=img_crs)

    return gdf


def _unpack_point_shapefiles(shapefile):
    """
    Helper function for opening and unpacking Point and Multi-Point type shapefile data

    Keyword inputs:
    Inputs:
    shapefile: Fiona formatted shapefile data 

    :param shapefile: class 'fiona.collection.Collection'
    :return coordinates: list
    """
    if type(shapefile[0]['geometry']['coordinates']) is list:
        coordinates = [shape['geometry']['coordinates'] for shape in shapefile]
    if type(shapefile[0]['geometry']['coordinates']) is tuple:
        coordinates = [[shape['geometry']['coordinates']] for shape in shapefile]
    return coordinates
