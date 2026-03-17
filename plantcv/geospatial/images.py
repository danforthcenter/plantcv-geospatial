# Sets up image classes as subclasses of numpy.ndarray

import numpy as np

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
                crs : str, transform : affine.Affine):
        # Create an instance of Image with default attributes
        obj = Image.__new__(cls, input_array, filename)
        # Add HSI-specific attributes
        obj.wavelengths = wavelengths
        obj.crs = crs
        obj.transform = transform
        return obj

    def __init__(self, **kwargs):
        self.thumb = self._create_thumb()

    def get_wavelength(self, wavelength):
        idx = np.abs(np.array(self.wavelengths) - wavelength).argmin()
        obj = super(GEO, self).__getitem__(np.s_[:, :, idx])
        obj.wavelengths = [self.wavelengths[idx]]
        obj.min_wavelength = np.min(obj.wavelengths)
        obj.max_wavelength = np.max(obj.wavelengths)
        return obj

    def _create_thumb(self):
        if len(self.default_wavelengths) == 3:
            thumb = BGR(input_array=np.dstack([self.get_wavelength(self.default_wavelengths[0]),
                                               self.get_wavelength(self.default_wavelengths[1]),
                                               self.get_wavelength(self.default_wavelengths[2])]),
                        filename=self.filename)
        else:
            thumb = GRAY(input_array=self.get_wavelength(self.default_wavelengths[0]),
                         filename=self.filename)
        return thumb
    