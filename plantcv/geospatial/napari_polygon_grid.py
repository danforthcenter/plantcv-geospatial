# Takes a viewer object with lines from napari_grid and turns those intersections into polygons

import numpy as np
from plantcv.plantcv import fatal_error


def _lineintersect(array1, array2):
    """Find the intersection point of two lines defined by their endpoints.

    Parameters
    ----------
    array1 : list of list of float
        Endpoints of the first line, as [[x0, y0], [x1, y1]].
    array2 : list of list of float
        Endpoints of the second line, as [[x0, y0], [x1, y1]].

    Returns
    -------
    [x,y] : list
        X and Y coordinate of the intersection point, as [x, y].
    """
    a1 = array1[1][1] - array1[0][1]
    b1 = array1[0][0] - array1[1][0]
    c1 = (a1*array1[0][0]) + (b1*array1[0][1])

    a2 = array2[1][1] - array2[0][1]
    b2 = array2[0][0] - array2[1][0]
    c2 = (a2*array2[0][0]) + (b2*array2[0][1])

    determinant = (a1*b2) - (a2*b1)

    if determinant == 0:
        fatal_error("Lines are parallel, no intersection exists.")

    x = (b2*c1 - b1*c2)/determinant
    y = (a1*c2 - a2*c1)/determinant
    return [x, y]


def napari_polygon_grid(viewer, layername="Shapes"):
    """Create a grid of polygons from grid lines in a Napari viewer.

    Reads lines from two Shapes layers named 'grid_lines1' and 'grid_lines2',
    computes their pairwise intersections, and adds the resulting polygons as
    a new Shapes layer.

    Parameters
    ----------
    viewer : napari.Viewer
        Napari viewer containing Shapes layers named 'grid_lines1' and
        'grid_lines2', each holding lines that form a grid.
    layername : str, optional
        Name for the new Shapes layer added to the viewer. Default is "Shapes".

    Returns
    -------
    None
        Polygons are added directly to the viewer as a side effect.
    """

    linelist1 = viewer.layers["grid_lines1"].data
    linelist2 = viewer.layers["grid_lines2"].data

    polygonlist = []
    for i in range(len(linelist1)-1):
        for j in range(len(linelist2)-1):
            point1 = _lineintersect(linelist1[i], linelist2[j])
            point2 = _lineintersect(linelist1[i+1], linelist2[j])
            point3 = _lineintersect(linelist1[i+1], linelist2[j+1])
            point4 = _lineintersect(linelist1[i], linelist2[j+1])
            points = [point1, point2, point3, point4, point1]
            polygonlist.append(np.array(points))

    shapes_layer = viewer.add_shapes(name=layername)
    # add mixed shapes using the `add` method
    shapes_layer.add(
        polygonlist,
        shape_type='polygon')
