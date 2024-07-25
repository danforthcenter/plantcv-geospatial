import rasterio
import fiona
from rasterio.mask import mask


def transform_points(img, geojson):
    """Takes a points-type shape file and makes circular rois using the points as centers.
    Inputs:
    image:      A spectral object from read_geotif.
    mask:       Binary mask from the same image.
    shapefile:  Path to the shape file containing the points.
    radius:     Radius of the desired ROI, to be used by plantcv's roi.multi
    
    Returns:
    roi_objects: = a dataclass with roi objects and hierarchies
    
    :return roi_objects: plantcv.plantcv.classes.Objects
    :param image: [spectral object]
    :param mask: [numpy ndarray]
    :return spectral_array: __main__.Spectral_data
    """
    geo_transform = img.geo_transform
    coord = []
    with fiona.open(geojson, 'r') as shapefile:
        for i in range(len(shapefile)):
            pixel_point = ~(geo_transform) * (shapefile[i].geometry["coordinates"])
            rounded = (int(pixel_point[0]), int(pixel_point[1]))
            coord.append(rounded)

    return coord
