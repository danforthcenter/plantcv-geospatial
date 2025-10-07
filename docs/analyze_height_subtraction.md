## Analyze height by subtraction to get a canopy height model (CHM)

Create canopy height model (CHM) from bare soil and plant height digital elevation model (DEM) or digital surface model (DSM) images. Calculates the soil elevation as a subtraction of the DSM with plant height from the DSM with bare soil. 
Note: the input DSMs need to be the same shape.

**plantcv.geospatial.analyze.height_subtraction**(*dsm1, dsm0*)

**returns** [PlantCV Spectral_data](https://plantcv.readthedocs.io/en/latest/Spectral_data/) object where the data_array attribute is the subtracted CHM.

- **Parameters:**
    - dsm1 - Spectral image object from a time point with plants, likely read in with [`geo.read_geotif`](read_geotif.md)
    - dsm0 - Spectral image object from a time point with bare ground, likely read in with [`geo.read_geotif`](read_geotif.md)

- **Context:**
    - This function will output a spectral image object that can then be used with other functions to analyze plant height within a given area.

```python
import plantcv.geospatial as gcv
import plantcv.plantcv as pcv

# Read in dsm as geotif
dsm1 = gcv.read_geotif(filename="./data/example_dsm.tif", bands=[0])
dsm0 = gcv.read_geotif(filename="./data/example_dsm.tif", bands=[0])

# To get the canopy height model:
pcv.params.debug = "plot"

chm = gcv.analyze.height_subtraction(dsm1, dsm0)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/analyze/dsm.py)
