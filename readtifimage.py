#Read TIF image

import rasterio


def readimage(filepath):
   """Read TIF image from file.

    Inputs:
    filepath = path of TIF image file

    Returns:
    imagearray = image object as numpy array
    crs = coordinate reference system
    width = width of digital number array values
    height = height of digital number array values
    bands = total number of bands in image
    bounds = spatial extent of the image mapped on the earth's surface

    :param filename: str
    :return imagearray: numpy.ndarray
    :return crs: rasterio.crs.CRS
    :return width: int
    :return height: int
    :return bands: int
    :return bounds: rasterio.coords.BoundingBox
    """
   img = rasterio.open(filepath)
   inputarray = img.read()
   crs = img.crs
   width = img.width
   height = img.height
   bands = img.count
   bounds = img.bounds
   
   return inputarray, crs, width, height, bands, bounds
    