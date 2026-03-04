# Takes a napari viewer object with polygons and turns the points into rois

import shapely
from plantcv.plantcv.roi import multi, circle
from shapely.geometry import Polygon


def center_grid_rois(img, viewer, radius=10, layername="Shapes"):
    """Create circular ROIs centered at the centroids of polygon shapes.

    Extracts the centroid from each polygon in a shapes layer and creates
    circular regions of interest (ROIs) at those points.

    Parameters
    ----------
    img : numpy.ndarray
        Input image on which the ROIs will be drawn.
    viewer : napari.Viewer
        Napari viewer object containing a shapes layer with polygons.
        Typically the output from napari_polygon_grid.
    radius : int
        Radius of the circular ROIs in pixels.
    layername : str, optional
        Name of the shapes layer to use. Default is "Shapes".

    Returns
    -------
    rois : plantcv.plantcv.classes.Objects
        Multi-ROI object containing all circular regions of interest and
        their hierarchical relationships.
    """
    points_list = []
    for i in viewer.layers[layername].data:
        point = shapely.centroid(Polygon(i))
        points_list.append((point.coords[0][1], point.coords[0][0]))
    if len(points_list) > 1:
        return multi(img=img, coord=points_list, radius=radius)
    return circle(img=img, x=int(points_list[0][0]),
                  y=int(points_list[0][1]), r=radius)
