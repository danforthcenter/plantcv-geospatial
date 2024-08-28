# Transform georeferenced GeoJSON/shapefile points into python coordinates
import fiona


def transform_points(img, geojson):
    """Takes a points-type shapefile/GeoJSON and transforms to numpy coordinates
    Inputs:
    img:        A spectral object from read_geotif.
    geojson:    Path to the shape file containing the points.

    Returns:
    coord:      Transformed points as a list of numpy coordinates

    :param img: [spectral object]
    :param geojson: str
    :return coord: list
    """
    geo_transform = img.geo_transform

    coord = []
    with fiona.open(geojson, 'r') as shapefile:
        for i, _ in enumerate(shapefile):
            if type((shapefile[i].geometry["coordinates"])) is list:
                pixel_point = ~(geo_transform) * (shapefile[i].geometry["coordinates"][0])
            if type((shapefile[i].geometry["coordinates"])) is tuple:
                pixel_point = ~(geo_transform) * (shapefile[i].geometry["coordinates"])
            rounded = (int(pixel_point[0]), int(pixel_point[1]))
            coord.append(rounded)

    return coord
