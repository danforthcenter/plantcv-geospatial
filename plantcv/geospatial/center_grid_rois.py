# Takes a napari viewer object with polygons and turns the points into rois

import plantcv.plantcv as pcv
import shapely
from shapely.geometry import Polygon


def center_grid_rois(img, viewer, radius=10):
    points_list = []
    for i in viewer.layers["grid_shapes"].data:
        point = shapely.centroid(Polygon(i))
        points_list.append((point.coords[0][1],point.coords[0][0]))
    rois = pcv.roi.multi(img=img, coord=points_list, radius=radius)
    return rois
