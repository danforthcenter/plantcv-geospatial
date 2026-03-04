# Transform georeferenced GeoJSON/shapefile polygons into python coordinates
import fiona


def transform_polygons(img, geojson):
    """
    Transform a polygon or multipolygon shapefile or GeoJSON into image pixel coordinates.

    Parameters
    ----------
    img : spectral object
        A spectral image object returned by ``read_geotif``.
    geojson : str
        Path to the shapefile or GeoJSON file containing polygon or multipolygon geometries.

    Returns
    -------
    coord : list of list of list of int
        Pixel coordinates as a list of polygons, where each polygon is a list
        of ``[col, row]`` integer pairs. The closing vertex of each polygon
        is dropped to avoid duplication.
    """
    geo_transform = img.metadata["transform"]
    coord = []
    with fiona.open(geojson, 'r') as shapefile:
        for row in shapefile:
            temp_list = []
            # Polygon
            if len(row.geometry["coordinates"][0]) > 1:
                square = row.geometry["coordinates"][0][:-1]
            # Multi Polygon
            else:
                square = row.geometry["coordinates"][0][0][:-1]
            for j in square:
                vertex = ~(geo_transform) * j
                temp_list.append([int(vertex[0]), int(vertex[1])])
            coord.append(temp_list)
    return coord
