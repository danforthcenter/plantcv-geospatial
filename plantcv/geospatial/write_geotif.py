# Write image data out to a GeoTIFF file
import os
import numpy as np
import rasterio
from plantcv.geospatial.images import GEO, DSM
from plantcv.plantcv import fatal_error


def write_geotif(path, img, transform=None, crs=None, nodata=None):
    """Write image data to a new GeoTIFF file.

    Parameters
    ----------
    path : str
        Output file path. Parent directories are created if they don't already exist.
    img : numpy.ndarray, plantcv.geospatial.images.GEO, or plantcv.geospatial.images.DSM
        Image data to write, shape (H, W) or (H, W, bands). If a GEO or DSM object
        is given, `transform`, `crs`, and `nodata` are taken from that object's own
        attributes unless explicitly overridden below.
    transform : affine.Affine, optional
        Transformation matrix from array coordinates to geospatial coordinates
    crs : rasterio.crs.CRS or str, optional
        Coordinate reference system to tag the output with. Required if `img` is a
        plain array; optional (and overrides the object's own crs) if `img` is a
        GEO or DSM object.
    nodata : float, optional
        Nodata value to record in the output file's metadata. Optional.
    """
    if isinstance(img, (GEO, DSM)):
        # Overwrite metadata with image attributes
        transform = img.transform if transform is None else transform
        crs = img.crs if crs is None else crs
        nodata = img.nodata if nodata is None else nodata
        # Plain array for downstream
        array = np.asarray(img)
    else:
        array = img
        if transform is None or crs is None:
            fatal_error("`transform` and `crs` are required.")

    if array.ndim == 2:
        # rasterio always wants a band axis, even for single-band data.
        array = array[:, :, np.newaxis]
    height, width, bands = array.shape
    # Change band order for rasterio.
    band_first = np.moveaxis(array, -1, 0)

    out_dir = os.path.dirname(path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with rasterio.open(path, "w", driver="GTiff", height=height, width=width, count=bands,
                       dtype=band_first.dtype, crs=crs, transform=transform, nodata=nodata) as dst:
        dst.write(band_first)
