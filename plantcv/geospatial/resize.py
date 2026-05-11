# Resize geospatial image classes

import numpy as np
import affine as affine_module
from plantcv.plantcv.transform import resize as pcv_resize
from plantcv.geospatial.images import GEO, DSM


def resize(img, size, interpolation="auto"):
    """Resize a geospatial image to a desired new size.

    Wraps plantcv.plantcv.transform.resize and preserves geospatial metadata
    for GEO and DSM objects by updating the affine transform to reflect the
    new pixel resolution.

    Parameters
    ----------
    img : plantcv.geospatial.images object, either GEO or DSM
        A GEO image object returned by ``read_geotif``.
    size : tuple of ints         
        Output image size in pixels (width, height)
    interpolation: str
        Interpolation method:
        "auto" = select method automatically (default)
        "area" = resampling using pixel area (OpenCV INTER_AREA)
        "bicubic" = bicubic interpolation (OpenCV INTER_CUBIC)
        "bilinear" = bilinear interpolation (OpenCV INTER_LINEAR)
        "lanczos" = Lanczos interpolation (OpenCV INTER_LANCZOS4)
        "nearest" = nearest-neighbor interpolation (OpenCV INTER_NEAREST)
        None = disable interpolation and crop or pad instead

    Returns
    ---------- 
    resized_img : plantcv.geospatial.images object, either GEO or DSM
        Resized image of the same class as the input
    """
    orig_h, orig_w = img.shape[:2]
    new_w, new_h = size

    resized_array = pcv_resize(np.asarray(img), size=size, interpolation=interpolation)

    if isinstance(img, GEO):
        new_transform = _scale_transform(img.transform, orig_w, orig_h, new_w, new_h)
        return GEO(
            input_array=resized_array,
            filename=img.filename,
            wavelengths=img.wavelengths,
            default_wavelengths=img.default_wavelengths,
            crs=img.crs,
            transform=new_transform,
            nodata=getattr(img, "nodata", None)
        )
    elif isinstance(img, DSM):
        new_transform = _scale_transform(img.transform, orig_w, orig_h, new_w, new_h)
        return DSM(
            input_array=resized_array,
            filename=img.filename,
            crs=img.crs,
            transform=new_transform,
            cutoff=getattr(img, "cutoff", None),
            nodata=getattr(img, "nodata", None)
        )


def _scale_transform(transform, orig_w, orig_h, new_w, new_h):
    """Scale an affine transform to reflect a change in image dimensions.
    Parameters
    ----------
    transform : affine.Affine
        Affine transformation matrix of original image.
    orig_w : int         
        Original image width.
    orig_h : int
        Original image height.
    new_w : int
        New image width.
    new_h : int
        New image height.

    Returns
    ---------- 
    transform : affine.Affine
        Rescaled transformation matrix.
    """
    if transform is None:
        return None
    return affine_module.Affine(
        transform.a * (orig_w / new_w),
        transform.b,
        transform.c,
        transform.d,
        transform.e * (orig_h / new_h),
        transform.f
    )
