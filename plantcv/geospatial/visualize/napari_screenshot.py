# Visualization tool to use Napari screenshot for visualizing polygons in a shapefile

import napari
import os
import numpy as np
from plantcv.geospatial import transform_polygons
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def napari_screenshot(img, geojson, shape_type="polygon"):
    """Takes a screenshot of a napari viewer window with plotted shapefile shapes

    Parameters
    ----------
    img : PlantCV spectral object
        Read in geotif
    geojson : str
        Path to a geojson or shapefile containing shapes
    shape_type: str
        Type of shape contained in the shapefile, default to "polygon"

    Returns
    -------
    cropped: numpy.ndarray
        Screenshot of Napari window with shapes plotted
    """
    # Read in coordinates
    coords = transform_polygons(img=img, geojson=geojson)
    # Transform coordinates for Napari
    corrected_coords = []
    for i in coords:
        newpoly = []
        for j in i:
            newpoly.append([j[1], j[0]])
        corrected_coords.append(newpoly)
    # Take Napari screenshot
    viewer = napari.Viewer()
    viewer.add_image(img.pseudo_rgb)
    viewer.add_shapes(corrected_coords, shape_type=shape_type)
    screen = viewer.screenshot()
    viewer.close()
    # Crop to image since Napari zooms out by default
    screen = screen[:, :, :3]

    non_zero_rows = np.any(screen != 0, axis=(1, 2))
    non_zero_cols = np.any(screen != 0, axis=(0, 2))

    # Get indices of non-zero rows and columns
    row_indices = np.where(non_zero_rows)[0]
    col_indices = np.where(non_zero_cols)[0]

    # Get bounds
    row_min, row_max = row_indices[0], row_indices[-1] + 1
    col_min, col_max = col_indices[0], col_indices[-1] + 1

    # Return trimmed image
    cropped = screen[row_min:row_max, col_min:col_max]

    _debug(visual=cropped, filename=os.path.join(params.debug_outdir, f"{params.device}_screenshot.png"))
    return cropped
