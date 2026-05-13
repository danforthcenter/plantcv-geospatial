# Subtract DSMs to create a Canopy Height Model
from plantcv.plantcv import params, fatal_error
from plantcv.plantcv._debug import _debug
import numpy as np
import os


def subtract_dsm(dsm1, dsm0):
    """
    A function that subtracts the height of one DSM from the height of another.
    Outputs a DSM object representing the canopy height model.

    Parameters
    ----------
    dsm1 : plantcv.geospatial.images.DSM object
        Digital surface model data, generally from read_geotif, DSM with plant height
    dsm0 : plantcv.geospatial.images.DSM object
        Digital surface model data, generally from read_geotif, DSM of bare ground

    Returns
    -------
    subtracted_dsm : plantcv.geospatial.images.DSM object
        New DSM image object with dsm1 - dsm0
    """
    # Check the coordinate reference system (CRS) is the same for both of the DSMs
    if dsm1.crs != dsm0.crs:
        fatal_error("The two input DSMs do not have the same coordinate reference system (CRS).")

    # Check for equal arrays
    if np.array_equal(dsm1, dsm0, equal_nan=True):
        print("Warning: dsm1 and dsm0 have identical array_data, result will be flat.")

    # Check the shapes are equivalent
    if (dsm1.shape == dsm0.shape) is False:
        fatal_error("Input DSMs do not have same shape, can be changed with PCV 'resize' function.")

    # Perform the subtraction
    final_data = dsm1 - dsm0

    # Fill in attributes

    final_data.__init__(input_array=final_data, filename=None, crs=dsm1.crs,
                        transform=dsm1.transform, cutoff=dsm1.cutoff, nodata=dsm1.nodata)

    _debug(visual=final_data.thumb, filename=os.path.join(params.debug_outdir, f"{params.device}_substracted_dsm.png"))
    return final_data