# Takes a viewer object with lines from napari_grid and turns those intersections into polygons

import numpy as np
from plantcv.plantcv import fatal_error


def _lineintersect(array1, array2):
    """Takes in two lines in the form of end point lists and finds the intersection.

    Parameters
    ----------
    array1 : list
        Endpoints of first line
    array2 : list
        Endpoints of second line

    Returns
    -------
    [x,y] : list
        X and Y coordinate of the intersection point
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
        return None
    else:
        x = (b2*c1 - b1*c2)/determinant
        y = (a1*c2 - a2*c1)/determinant
        return [x, y]


def napari_polygon_grid(viewer, numdivs):
    """Creates a grid of polygons in a Napari viewer.

    Parameters
    ----------
    viewer : Napari viewer object
        Viewer with a Shapes layer called "grid_lines" with lines in a grid
    numdivs : list of length 2
        Number of divisions along the first and second axis of the field polygon.

    Returns
    -------
    None
    """
    linelist1 = viewer.layers["grid_lines"].data[:numdivs[0]+1]
    linelist2 = viewer.layers["grid_lines"].data[numdivs[0]+1:]

    polygonlist = []
    for i in range(len(linelist1)-1):
        for j in range(len(linelist2)-1):
            point1 = _lineintersect(linelist1[i], linelist2[j])
            point2 = _lineintersect(linelist1[i+1], linelist2[j])
            point3 = _lineintersect(linelist1[i+1], linelist2[j+1])
            point4 = _lineintersect(linelist1[i], linelist2[j+1])
            points = [point1, point2, point3, point4, point1]
            polygonlist.append(np.array(points))

    shapes_layer = viewer.add_shapes(name='grid_shapes')
    # add mixed shapes using the `add` method
    shapes_layer.add(
        polygonlist,
        shape_type='polygon')
