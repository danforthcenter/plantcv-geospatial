# Sets up image classes as subclasses of numpy.ndarray

import numpy as np
import affine

class Image(np.ndarray):
    """The generic Image class extends the np.ndarray class by adding attributes."""

    # From NumPy documentation
    # Add filename attribute
    def __new__(cls, input_array: np.ndarray, filename: str):
        obj = np.asarray(input_array).view(cls)
        # New attribute filename stores the path and filename of the source file
        obj.filename = filename
        return obj

    def __array_finalize__(self, obj):
        if obj is not None:
            self.filename = getattr(obj, "filename", None)

    def __getitem__(self, key):
        # Enhance the np.ndarray __getitem__ method
        # Slice the array as requested but return an array of the same class
        # Idea from NumPy examples of subclassing:
        value = super(Image, self).__getitem__(key)
        return value
    
class GEO(Image):
    """Subclass of Image for geospatial images."""
    
    def __new__(cls, input_array: np.ndarray, filename: str, wavelengths: list, 
                default_wavelengths : list, channels : list, crs : str, 
                transform : affine.Affine):
        # Create an instance of Image with default attributes
        obj = Image.__new__(cls, input_array, filename)
        # Add HSI-specific attributes
        obj.wavelengths = wavelengths
        obj.default_wavelengths = default_wavelengths
        obj.channels = channels
        obj.crs = crs
        obj.transform = transform
        return obj

    def __init__(self, **kwargs):
        self.thumb = self._create_thumb()

    def get_wavelength(self, wavelength):
        idx = np.abs(np.array(self.wavelengths) - wavelength).argmin()
        obj = super(GEO, self).__getitem__(np.s_[:, :, idx])
        return obj

    def _create_thumb(self):
        thumb = np.dstack([self.get_wavelength(self.default_wavelengths[0]),
                           self.get_wavelength(self.default_wavelengths[1]),
                           self.get_wavelength(self.default_wavelengths[2])])
        return thumb

class DSM(Image):
    """Subclass of Image for digital surface models."""
    
    def __new__(cls, input_array: np.ndarray, filename: str, crs : str, 
                transform : affine.Affine, cutoff : float):
        # Create an instance of Image with default attributes
        obj = Image.__new__(cls, input_array, filename)
        # Add HSI-specific attributes
        obj.crs = crs
        obj.transform = transform
        obj.cutoff = cutoff
        return obj

    def __init__(self, **kwargs):
        self.data_array = self._gray_cutoff()
        self.thumb = self._create_thumb()
        
    def _gray_cutoff(self):
        img_copy = np.squeeze(self.input_array)
        if self.cutoff is not None :
            quantile = np.quantile(img_copy, self.cutoff)
            img_copy[img_copy >= quantile] = np.nan
        return img_copy

    def _create_thumb(self):
        img_copy = self.data_array
        # Change nodata values to Nan
        img_copy[img_copy == min(np.unique(img_copy))] = np.nan
        # Stretch values to min/max for visualization
        img_copy = 255*((img_copy - np.nanmin(img_copy)) / (np.nanmax(img_copy) - np.nanmin(img_copy)))
        # Return nodata values to 0
        img_copy = np.nan_to_num(img_copy, nan=0.0)
        # Convert to uint8
        thumb = img_copy.astype(np.uint8)
        return thumb
    