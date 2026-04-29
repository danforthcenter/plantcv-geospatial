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
                default_wavelengths : list, crs : str, transform : affine.Affine, nodata : float):
        # Create an instance of Image with default attributes
        obj = Image.__new__(cls, input_array, filename)
        # Add GEO-specific attributes
        obj.wavelengths = wavelengths
        obj.default_wavelengths = default_wavelengths
        obj.crs = crs
        obj.transform = transform
        obj.nodata = nodata
        return obj

    def __init__(self, input_array: np.ndarray, filename: str, wavelengths: list,
                 default_wavelengths: list, crs: str, transform: affine.Affine, nodata: float):
        super().__init__()
        self.thumb = self._create_thumb()

    def __array_finalize__(self, obj):
        super().__array_finalize__(obj)
        if obj is not None:
            self.wavelengths = getattr(obj, "wavelengths", None)
            self.default_wavelengths = getattr(obj, "default_wavelengths", None)
            self.crs = getattr(obj, "crs", None)
            self.transform = getattr(obj, "transform", None)
            self.nodata = getattr(obj, "nodata", None)

    def get_wavelength(self, wavelength):
        """Finds channel closest to a provided numerical wavelength

        Parameters
        ----------
        wavelength : int
            Desired wavelength

        Returns
        -------
        numpy.ndarray
            2D array from channel closest to wavelength
        """
        idx = np.abs(np.array(self.wavelengths) - wavelength).argmin()
        obj = super(GEO, self).__getitem__(np.s_[:, :, idx])
        return obj

    def _create_thumb(self):
        """Creates a pseudo_rgb thumbnail image for debugging

        Returns
        -------
        numpy.ndarray
            Thumbnail image
        """
        thumb = np.dstack([self.get_wavelength(self.default_wavelengths[0]),
                           self.get_wavelength(self.default_wavelengths[1]),
                           self.get_wavelength(self.default_wavelengths[2])])
        thumb[thumb == self.nodata] = 0
        return thumb


class DSM(Image):
    """Subclass of Image for digital surface models."""

    def __new__(cls, input_array: np.ndarray, filename: str, crs : str,
                transform : affine.Affine, cutoff : float, nodata : float):
        # Create an instance of Image with default attributes
        obj = Image.__new__(cls, input_array, filename)
        # Add HSI-specific attributes
        obj.crs = crs
        obj.transform = transform
        obj.cutoff = cutoff
        obj.nodata = nodata
        return obj

    def __init__(self, input_array: np.ndarray, filename: str, crs: str,
                 transform: affine.Affine, cutoff: float, nodata: float):
        super().__init__()
        self.data_array = self._gray_cutoff()
        self.thumb = self._create_thumb()

    def __array_finalize__(self, obj):
        super().__array_finalize__(obj)
        if obj is not None:
            self.crs = getattr(obj, "crs", None)
            self.transform = getattr(obj, "transform", None)
            self.cutoff = getattr(obj, "cutoff", None)
            self.nodata = getattr(obj, "nodata", None)

    def _gray_cutoff(self):
        """Converts all pixels in a dsm above a value threshold to no data.

        Returns
        -------
        numpy.ndarray
            DSM with values above threshold converted to no data
        """
        img_copy = np.squeeze(self)
        if self.cutoff is not None :
            quantile = np.quantile(img_copy, self.cutoff)
            img_copy[img_copy >= quantile] = np.nan
        return img_copy

    def _create_thumb(self):
        """Creates a stretched DSM for visualization.

        Returns
        -------
        numpy.ndarray
            Stretched thumbnail
        """
        img_data = self.data_array
        # make masked array for nodata values
        mask = np.where(img_data == self.nodata, 1, 0)
        mx = np.ma.masked_array(img_data, mask)
        # get range of masked array for visualization
        mxmin = mx.min()
        mxmax = mx.max()
        # make copy of image squashed into uint8 range
        img_copy = 255 * ((mx - mxmin) / (mxmax - mxmin))
        # Convert to uint8
        thumb = img_copy.astype(np.uint8)
        # remove data from masked array
        thumb = thumb.data
        # slice 0s in for no-data
        thumb = np.where(mask == 1, 0, thumb)
        return thumb
