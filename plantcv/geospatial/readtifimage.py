# Read TIF File
import rasterio


def readimage(filepath):
    """Read TIF image from file.

    Inputs:
    filepath: Path of the TIF image file.

    Returns:
    imagearray: Image object as numpy array.
    height: Height of digital number array values.
    width: Width of digital number array values.
    bands: Total number of bands in the image.

    :param filepath: str
    :return imagearray: numpy.ndarray, height: int, width: int, bands: int
    """
    img = rasterio.open(filepath)
    inputarray = img.read()
    height = img.height
    width = img.width
    bands = img.count
    return inputarray, height, width, bands
