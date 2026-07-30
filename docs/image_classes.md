## Geospatial Image Classes

### class `Image`

A PlantCV-geospatial object class extending numpy ndarray objects.

*class* plantcv.geospatial.**Image**

`Image` is a class that extends a numpy array to include a filename attributed and to return another `Image` class object when sliced. This class is used to create `GEO` and `DSM` objects, which extend it to include relevant metadata for geotiff files or digital surface models.

#### Attributes

Attributes are accessed as image.*attribute*

- **filename**: Path to the file used to generate this object.

### class `GEO`

A PlantCV-geospatial object class extending the `plantcv.geospatial.Image` class.

*class* plantcv.geospatial.**GEO**

The `GEO` class holds image data in an easy to access way, including several important features of geotiff or netcdf data as added attributes.

#### Attributes

Attributes are accessed as GEO.*attribute*.

- **wavelengths**: A list of wavelengths (int) included in the array_data.

- **default_wavelengths**: A list of default wavelengths, used to create a thumbnail image.

- **crs**: A Coordinate Reference System to map the geotiff between numpy coordinates and physical coordinates.

- **transform**: An `affine.Affine` object specifying any transformation.

- **thumb**: A thumbnail image in 3 channels defined by `default_wavelengths`. Similar to a psuedo-rgb image from the `plantcv.plantcv.Spectral_data` class.

### class `DSM`

A PlantCV-geospatial object class extending the `plantcv.geospatial.Image` class.

*class* plantcv.geospatial.**DSM**

The `DSM` class holds digital surface/texture/elevation model (dsm, dtm, dem) data in an easy to access way, including several important features of dsm data as added attributes.

#### Attributes

Attributes are accessed as DSM.*attribute*.

- **crs**: A Coordinate Reference System to map the geotiff between numpy coordinates and physical coordinates.

- **transform**: An `affine.Affine` object specifying any transformation.

- **cutoff**: A cutoff for how high a pixel can be, pixels above this height will be converted to `numpy.nan`.

- **thumb**: A grayscale thumbnail image of the DSM.


**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/images.py)
