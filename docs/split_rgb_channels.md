## Split Pseudo-RGB Channels

Split the pseudo-RGB image in a geospatial `Spectral_data` object into red, green, and blue grayscale channels.

**plantcv.geospatial.split_rgb_channels**(*img, as_float=True*)

**returns** `tuple` of grayscale channel images: `(r_channel, g_channel, b_channel)`.

- **Parameters:**
    - img - A [PlantCV Spectral_data](https://docs.plantcv.org/en/stable/Spectral_data/) object from `read_geotif` or `read_netcdf`.
    - as_float - If `True` (default), return channels as `numpy.float32` for index calculations. If `False`, keep original dtype.

- **Example use:**

```python
import plantcv.geospatial as gcv

# Read geotif in
ortho1 = gcv.read_geotif(filename="./data/example_img.tif", bands="R,G,B")

# Split pseudo-rgb channels
r_channel, g_channel, b_channel = gcv.split_rgb_channels(img=ortho1)
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/split_rgb_channels.py)
