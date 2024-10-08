# Transform georeferenced GeoJSON/shapefile polygons into python coordinates
import fiona


def transform_polygons(img, geojson):
    """Takes a polygon or multi polygon-type shapefile/GeoJSON and transforms to numpy coordinates
    Inputs:
    img:        A spectral object from read_geotif.
    geojson:    Path to the shape file containing the points.

    Returns:
    coord:      Transformed polygons as a list of lists of numpy coordinates

    :param img: [spectral object]
    :param geojson: str
    :return coord: list
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
