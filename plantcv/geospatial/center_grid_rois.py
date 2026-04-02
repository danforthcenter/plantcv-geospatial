# Takes a napari viewer object with polygons and turns the points into rois

import cv2
import numpy as np
from shapely import centroid
from shapely.geometry import Polygon
from plantcv.plantcv import fatal_error
from plantcv.plantcv.roi import multi, circle


def center_grid_rois(editor, radius=10, layername="Shapes"):
    """Create circular ROIs centered at the centroids of polygon shapes.

    Parameters
    ----------
    editor : geospatial.create_shapes.interactive_shapes.InteractiveShapes
        InteractiveShapes object containing a layer with polygons
    radius : int, optional
        Radius of the circular ROIs in pixels. Default is 10.
    layername : str, optional
        Name of layer containing shapes to use. Default is "Shapes"

    Returns
    -------
    rois : plantcv.plantcv.classes.Objects
        Multi-ROI object containing all circular regions of interest
                  and their hierarchical relationships.
    """
    points_list = []
    for i in editor.viewer.layers[layername].data:
        point = centroid(Polygon(i))
        points_list.append((point.coords[0][1], point.coords[0][0]))

    if not points_list:
        fatal_error(f"No shapes found in layer '{layername}'.")

    debug_img = np.copy(editor.img.thumb)
    for x, y in points_list:
        cv2.circle(debug_img, (int(x), int(y)), radius, (255, 0, 0), 2)

    if len(points_list) > 1:
        return multi(img=editor.img.thumb, coord=points_list, radius=radius)

    return circle(img=editor.img.thumb, x=int(points_list[0][0]),
                  y=int(points_list[0][1]), r=radius)
