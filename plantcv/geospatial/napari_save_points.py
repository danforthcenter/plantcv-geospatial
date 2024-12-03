# Function to save out clicked points collected in napari

import plantcv.plantcv as pcv
from plantcv.plantcv import warn
from plantcv.geospatial import read_geotif
import napari
import os


def napari_save_points(images, num_points, outdir="./", bands="R,G,B"):
    """Opens a set of images one at a time in a Napari window, waits for users
    to click points and then saves those points to a file with the same name as the image.

    Args:
        images (list or str): Either a list of image paths or a directory name. 
        num_points (int): Number of points expected. If number of clicks received is different,
                        the image path is added to redo_list and returned.
        outdir (str, optional): Directory to save text files with points. Defaults to "./".
        bands (str, optional): Band list if input images are geotifs. Defaults to "R,G,B".

    Returns:
        list: List of images to be redone due to a different number of clicked points than expected.
    """
    # store debug
    debug = pcv.params.debug

    pcv.params.debug = None
    # Store images with mistakes to a new list
    redo_list = []

    image_paths = images
    if not isinstance(images, list):
        image_paths = [os.path.join(images, i) for i in os.listdir(images)]
    # Loop over each image
    for image_path in image_paths:
        # Load the current image
        img_type = (image_path.split("/")[-1]).split(".")[-1]
        if img_type == "tif":
            geo_image = read_geotif(image_path, bands=bands)
            image = geo_image.pseudo_rgb
        else:
            image, _, _ = pcv.readimage(image_path)
        # Save image name for output file
        img_name = (image_path.split("/")[-1]).split(".")[:-1]

        viewer = napari.Viewer()

        # Add the image and points layer
        viewer.add_image(image)
        viewer.add_points(name="points")
        viewer.show(block=True)

        # Save file if correct number of points
        if len(viewer.layers["points"].data) == num_points:
            with open(os.path.join(outdir, img_name[0]+"_warp.txt"), "w") as output:
                for i in viewer.layers["points"].data:
                    point = [i[1], i[0]]
                    output.write(str(point) + '\t')
        else:
            redo_list.append(image_path)
            warn('Image ' + str(image_path) + ' collected incorrect number of points. ' +
                 'Added to redo list.')
    # Reset debug
    pcv.params.debug = debug
    return redo_list
