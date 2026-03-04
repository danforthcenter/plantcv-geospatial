# Takes a napari viewer object with polygons and turns the points into rois

import cv2
import numpy as np
from shapely import centroid
from shapely.geometry import Polygon
from plantcv.plantcv import fatal_error
from plantcv.plantcv.roi import multi, circle


def center_grid_rois(img, viewer, radius=10, layername="Shapes"):
    """Create circular ROIs centered at the centroids of polygon shapes.
    Inputs:
    img         = Input image on which the ROIs will be drawn.
    viewer      = Napari viewer object containing a shapes layer with polygons.
                  Typically the output from napari_polygon_grid.
    radius      = Radius of the circular ROIs in pixels (optional, default=10).
    layername   = Name of the shapes layer to use (optional, default="Shapes").

    Returns:
    rois        = Multi-ROI object containing all circular regions of interest
                  and their hierarchical relationships.

    :param img: numpy.ndarray
    :param viewer: napari.Viewer
    :param radius: int
    :param layername: str
    :return rois: plantcv.plantcv.classes.Objects
    """
    points_list = []
    for i in viewer.layers[layername].data:
        point = centroid(Polygon(i))
        points_list.append((point.coords[0][1], point.coords[0][0]))

    if not points_list:
        fatal_error(f"No shapes found in layer '{layername}'.")

    debug_img = np.copy(img)
    for x, y in points_list:
        cv2.circle(debug_img, (int(x), int(y)), radius, (255, 0, 0), 2)

    if len(points_list) > 1:
        return multi(img=img, coord=points_list, radius=radius)
    return circle(img=img, x=int(points_list[0][0]),
                  y=int(points_list[0][1]), r=radius)
