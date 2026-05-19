# Resize geospatial image classes
import os
import cv2
import numpy as np
import affine as affine_module
from plantcv.plantcv.transform import resize as pcv_resize
from plantcv.plantcv.transform.resize import _set_interpolation
from plantcv.geospatial.images import GEO, DSM
from plantcv.plantcv import fatal_error, params
from plantcv.plantcv._debug import _debug


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

    # Suppress pcv_resize's raw-array debug — the thumb debug below replaces it
    saved_debug = params.debug
    params.debug = None
    nodata = getattr(img, "nodata", None)
    resized_array = _resize_array(np.asarray(img), size=size, interpolation=interpolation, nodata=nodata)
    params.debug = saved_debug

    if isinstance(img, GEO):
        new_transform = _scale_transform(img.transform, orig_w, orig_h, new_w, new_h)
        resized_img = GEO(
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
        resized_img = DSM(
            input_array=resized_array,
            filename=img.filename,
            crs=img.crs,
            transform=new_transform,
            cutoff=getattr(img, "cutoff", None),
            nodata=getattr(img, "nodata", None)
        )
    else:
        fatal_error("Input must be a GEO or DSM object.")
    _debug(visual=resized_img.thumb,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_thumbnail.png"))
    return resized_img


def _resize_array(arr, size, interpolation, nodata=None):
    """Resize a numpy array to size, handling images with more than 4 bands.

    cv2.resize is limited to 4 channels. For arrays with more bands, each
    channel is resized independently and the results are stacked.

    Parameters
    ----------
    arr : numpy.ndarray
        Image array with shape (H, W) or (H, W, bands).
    size : tuple of ints
        Output size in pixels (width, height).
    interpolation : str or None
        Interpolation method passed to pcv_resize / _set_interpolation.
    nodata : scalar, optional
        Nodata sentinel value. Nodata pixels are zero-filled before
        interpolation and restored afterward (via nearest-neighbor mask
        resize) so they cannot contaminate adjacent valid pixels.

    Returns
    ----------
    resized : numpy.ndarray
        Resized array.
    """
    # Replace nodata with a neutral fill before interpolation so that
    # averaging/area methods don't produce nodata-adjacent values.
    nodata_mask = None
    if nodata is not None:
        mask = arr == nodata
        if mask.any():
            nodata_mask = mask
            arr = arr.astype(np.float64)
            arr[nodata_mask] = 0

    if interpolation is not None and arr.ndim == 3 and arr.shape[2] > 4:
        interp_mtd = _set_interpolation(input_size=arr.shape[:2], output_size=size, method=interpolation)
<<<<<<< 142-resize-function-should-mask-nodata-values
        resized = np.dstack([cv2.resize(arr[:, :, i], dsize=size, interpolation=interp_mtd)
                             for i in range(arr.shape[2])])
    else:
        resized = pcv_resize(arr, size=size, interpolation=interpolation)
        if arr.ndim < 3 or arr.shape[2] <= 1:
            # Add empty third dimension back to match read in DSMs
            resized = np.expand_dims(resized, axis=-1)

    if nodata_mask is not None:
        # Resize mask with nearest-neighbor to keep nodata boundaries sharp.
        if nodata_mask.ndim == 3 and nodata_mask.shape[2] > 1:
            resized_mask = np.dstack([
                cv2.resize(nodata_mask[:, :, i].astype(np.uint8), dsize=size,
                           interpolation=cv2.INTER_NEAREST)
                for i in range(nodata_mask.shape[2])
            ]).astype(bool)
        else:
            band = nodata_mask[:, :, 0] if nodata_mask.ndim == 3 else nodata_mask
            resized_mask = cv2.resize(band.astype(np.uint8), dsize=size,
                                      interpolation=cv2.INTER_NEAREST).astype(bool)
            if resized.ndim == 3:
                resized_mask = resized_mask[:, :, np.newaxis]
        resized[resized_mask] = nodata

    return resized
=======
        return np.dstack([cv2.resize(arr[:, :, i], dsize=size, interpolation=interp_mtd)
                          for i in range(arr.shape[2])])
    resized = pcv_resize(arr, size=size, interpolation=interpolation)
    # Add empty third dimension back to match read in DSMs
    return np.expand_dims(resized, axis=-1)
>>>>>>> main


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
