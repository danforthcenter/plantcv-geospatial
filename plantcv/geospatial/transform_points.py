# Transform georeferenced GeoJSON/shapefile points into python coordinates
import fiona


def transform_points(img, geojson):
    """
    Transform a points-type shapefile or GeoJSON into image pixel coordinates.

    Parameters
    ----------
    img : spectral object
        A spectral image object returned by ``read_geotif``.
    geojson : str
        Path to the shapefile or GeoJSON file containing points.

    Returns
    -------
    coord : list of tuple of int
        Pixel coordinates as a list of ``(col, row)`` integer tuples,
        one per point feature in the input file.
    """
    geo_transform = img.metadata["transform"]

    coord = []
    with fiona.open(geojson, 'r') as shapefile:
        for row in shapefile:
            if type((row.geometry["coordinates"])) is list:
                pixel_point = ~(geo_transform) * (row.geometry["coordinates"][0])
            if type((row.geometry["coordinates"])) is tuple:
                pixel_point = ~(geo_transform) * (row.geometry["coordinates"])
            rounded = (int(pixel_point[0]), int(pixel_point[1]))
            coord.append(rounded)

    return coord
