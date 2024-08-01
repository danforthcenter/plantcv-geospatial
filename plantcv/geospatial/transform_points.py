import rasterio
import fiona
from rasterio.mask import mask


def transform_points(img, geojson):
    """Takes a points-type shape file and makes circular rois using the points as centers.
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
        for i in range(len(shapefile)):
            pixel_point = ~(geo_transform) * (shapefile[i].geometry["coordinates"])
            rounded = (int(pixel_point[0]), int(pixel_point[1]))
            coord.append(rounded)

    return coord
