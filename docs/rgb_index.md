## RGB Index Calculator

Calculate common RGB indices from a geospatial `Spectral_data` object by name.

**plantcv.geospatial.rgb_index**(*img, index, eps=1e-5*)

**returns** `numpy.ndarray` index image.

- **Parameters:**
    - img - A [PlantCV Spectral_data](https://docs.plantcv.org/en/stable/Spectral_data/) object from `read_geotif` or `read_netcdf`.
    - index - RGB index abbreviation:
        - `BI`: Brightness Index = `sqrt((R^2 + G^2 + B^2)/3)`
        - `SCI`: Soil Color Index = `(R-G)/(R+G)`
        - `GLI`: Green Leaf Index = `(2*G-R-B)/(2*G+R+B)`
        - `HI`: Primary Colors Hue Index = `(2*R-G-B)/(G-B)`
        - `NGRDI`: Normalized Green Red Difference Index = `(G-R)/(G+R)`
        - `SI`: Spectral Slope Saturation Index = `(R-B)/(R+B)`
        - `VARI`: Visible Atmospherically Resistant Index = `(G-R)/(G+R-B)`
        - `HUE`: Overall Hue Index = `atan(2*(B-G-R)/30.5*(G-R))`
        - `BG_RATIO`: Blue/Green ratio = `B/G`
        - `BGI`: Blue-Green index = `(G-B)/(G+B+1e-5)`
        - `VI`: Vegetation Index = `G - (B + R)/2`
        - `CI`: Chlorophyll Index = `(G/R) - 1`
    - eps - Small value added to denominators to avoid divide-by-zero.

- **Helper:**
    - `plantcv.geospatial.list_rgb_indices()` returns all supported index names.

- **Example use:**

```python
import plantcv.geospatial as gcv
import plantcv.plantcv as pcv

ortho1 = gcv.read_geotif(filename="./data/example_img.tif", bands="R,G,B")

# Calculate BGI directly by name
bgi = gcv.rgb_index(img=ortho1, index="BGI")
pcv.visualize.histogram(img=bgi, bins=60)

plant_mask = pcv.threshold.binary(gray_img=bgi, threshold=0.06, object_type="light")
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/rgb_index.py)
