# Takes a viewer object with the 4-sided field polygon shape and makes a grid of lines

import numpy as np


def napari_grid(viewer, numdivs, layername="Shapes"):
    # Field polygon
    field_poly = []
    for i in viewer.layers[layername].data[0]:
        field_poly.append(np.array((i[0], i[1])))
    # Along the first side
    # Diving each side by points
    divs1 = []
    divs1.append(list(zip(np.linspace(field_poly[0][0], field_poly[1][0], numdivs[0]+1),
                          np.linspace(field_poly[0][1], field_poly[1][1], numdivs[0]+1))))
    divs1.append(list(zip(np.linspace(field_poly[3][0], field_poly[2][0], numdivs[0]+1),
                          np.linspace(field_poly[3][1], field_poly[2][1], numdivs[0]+1))))

    linelist = []
    for i in range(len(divs1[0])):
        point1 = [divs1[0][i][0],divs1[0][i][1]]
        point2 = [divs1[1][i][0],divs1[1][i][1]]
        linelist.append(np.array([point1, point2]))

    # Along the second side
    divs2 = []
    divs2.append(list(zip(np.linspace(field_poly[1][0], field_poly[2][0], numdivs[1]+1),
                          np.linspace(field_poly[1][1], field_poly[2][1], numdivs[1]+1))))
    divs2.append(list(zip(np.linspace(field_poly[0][0], field_poly[3][0], numdivs[1]+1),
                          np.linspace(field_poly[0][1], field_poly[3][1], numdivs[1]+1))))

    for i in range(len(divs2[0])):
        point1 = [divs2[0][i][0],divs2[0][i][1]]
        point2 = [divs2[1][i][0],divs2[1][i][1]]

        linelist.append(np.array([point1, point2]))

    shapes_layer = viewer.add_shapes(name='grid_lines')
    # add mixed shapes using the `add` method
    shapes_layer.add(
        linelist,
        shape_type='line')
