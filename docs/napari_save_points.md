## Save Napari clicked points

Uses Napari to open a list of images one at a time. The user then clicks a defined number of points on each image, which are then saved to a text file with the same name as the image. To be used upstream of warp for geospatial images that are not georeferenced. 

**geospatial.napari_save_points**(*images, num_points, outdir="./", bands="R,G,B"*)

- **Parameters:**
    - images - Either a list of image paths or a directory where images are stored. Each image will be opened in sequence.
    - num_points - Integer of expected number of clicked points. For warping downstream, this should be minimally 4.
    - outdir - Directory to save output text files with saved points for each image. Defaults to "./".
    - bands - If input images are geotifs, this is the required band order for `plantcv.geospatial.read_geotif`. Not required if image type is not geotif. 

- **Outputs:**
    - redo_list - list of images to redo because the number of clicks did not match num_points. Useful if the user makes a mistake and would like to retry for a subset of images.

- **Context:**
    - Saved files can be used to warp all images to a specified reference image to bring all images to the same frame. This is useful for geospatial images that have not been georeferenced, as this approximates a version of what using ground control points achieves. 

- **Example use:**
    - below to click field corners


```python
import plantcv.geospatial as geo

# Make a list of images, can also be a directory
img_list = ["./image1.jpg", "./image2.jpg", "./image3.jpg", "./image4.jpg"]

# Opens a Napari window with a points layer for each image
# User should click reference points equal to num_points and then close the window, prompting the next one to open

redo_list = geo.napari_save_points(img_list, num_points=4, outdir="./")

# Text files with points are saved to outdir
# Output is a list of any images the user should redo

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/napari_save_points.py)