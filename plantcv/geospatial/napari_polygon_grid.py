# Takes a viewer object with lines from napari_grid and turns those intersections into polygons

import numpy as np


def _lineintersect(array1, array2):   #Arrays are two points - This will be private function
    a1 = array1[1][1] - array1[0][1]
    b1 = array1[0][0] - array1[1][0]
    c1 = (a1*array1[0][0]) + (b1*array1[0][1])

    a2 = array2[1][1] - array2[0][1]
    b2 = array2[0][0] - array2[1][0]
    c2 = (a2*array2[0][0]) + (b2*array2[0][1])

    determinant = (a1*b2) - (a2*b1)

    if determinant == 0:
        print("lines are parallel")   # Have to turn this into an error using plantcv's error messages
    else:
        x = (b2*c1 - b1*c2)/determinant
        y = (a1*c2 - a2*c1)/determinant
        return [x,y]

def napari_polygon_grid(viewer, numdivs):
    # MAKE THE LINELISTS FROM NAPARI IN CASE YOU CHANGE THEM
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
