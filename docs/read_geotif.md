## Read Geo-tif Data

Read in data (from tif format, most likely georeferenced image data). 

**plantcv.geospatial.read_geotif**(*filename, bands="R,G,B", cropto=None, cutoff=None*)

**returns** [PlantCV Spectral_data](https://plantcv.readthedocs.io/en/latest/Spectral_data/) object instance.

- **Parameters:**
    - filename - Path of the TIF image file.
    - bands - Comma separated string representing the order of image bands (e.g., `bands="R,G,B"`), or a list of wavelengths (e.g., `bands=[650, 560, 480]`)
        - Supported symbols (case insensitive) and their default wavelengths: 
            - "R" (red) = 650nm
            - "G" (green) = 560nm
            - "B" (blue) = 480nm
            - "RE" (rededge) = 717nm
            - "N" or "NIR" (near infrared) = 842nm
            - "mask" (a binary mask to represent regions of no data in the image) = 0nm
            - "gray" (a grayscale image, usually a digital surface or elevation model) = 0nm
    - cropto - A geoJSON-type shapefile to crop the input image as it is read in. Default is None.
    - cutoff - An optional cutoff (0-100) for removing noise from grayscale images. Points greater than the percentile will be removed from the array data.

- **Context:**
    - This function aims to handle variability in data type, depth, and common "No-Data" values of Geo-tifs. There is some flexibility in formats supported but we encourage people to reach out on [GitHub](https://github.com/danforthcenter/plantcv-geospatial/issues) and collaborate with the PlantCV community to expand our support.
    - Negative values are masked to a value of 0 to account for common no data values, and for errant negative values that can result from calibration since reflectance is bounded 0-1.
    - Utilizing `cropto` can significantly reduce the memory needed to run a geospatial workflow. 
    - Setting cutoff is useful if you have things like power lines in your image. The debug image will be scaled to min and max value after filtering, so it is useful for choosing an appropriate threshold. 

- **Example use:**
    - below

```python
import plantcv.geospatial as gcv

# Read geotif in
ortho1 = gcv.read_geotif(filename="./data/example_img.tif", bands="b,g,r,RE,NIR")
ortho2 = gcv.read_geotif(filename="./data/example_rgb_img.tif", bands="R,G,B,mask",
                         cropto="./shapefiles/experimental_bounds.geojson")
ortho3 = gcv.read_geotif(filename="./data/example_gray_img.tif", bands="gray", cutoff=99)

```

![Screenshot](documentation_images/multispec_pseudo_rgb.png)

![Screenshot](documentation_images/rgb.png)

![Screenshot](documentation_images/gray.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/read_geotif.py)
