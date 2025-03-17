# Takes a napari viewer object with polygons and turns the points into rois

import shapely
from plantcv.plantcv.roi import multi, circle
from shapely.geometry import Polygon


def center_grid_rois(img, viewer, radius=10):
    """Creates circular ROIs from the center points of polygons.

    Parameters
    ----------
    img : numpy.ndarray
        Image on which to draw the ROIs.
    viewer : Napari viewer object
        Viewer containing a shapes layer called "grid_shapes".
        Probably the output from napari_polygon_grid.
    radius : integer
        Width of the circular ROI in number of pixels

    Returns
    -------
    rois : plantcv.plantcv.classes.Objects
        Region of Interest object and heirarchies
    """
    points_list = []
    for i in viewer.layers["grid_shapes"].data:
        point = shapely.centroid(Polygon(i))
        points_list.append((point.coords[0][1], point.coords[0][0]))
    if len(points_list) > 1:
        return multi(img=img, coord=points_list, radius=radius)
    return circle(img=img, x=int(points_list[0][0]),
                  y=int(points_list[0][1]), r=radius)
