# Analyze distribution of values in a canopy height model over shapefile-defined regions
import os
import pandas as pd
import altair as alt
import numpy as np
from plantcv.plantcv import outputs, params
from plantcv.plantcv._debug import _debug
from plantcv.geospatial._helpers import _histogram_stats, _gather_ids
from rasterstats import zonal_stats


def chm(dsm, geojson, bins=10, label=None):
    """
    A function that analyzes height distribution in plots.

    Parameters
    ----------
    chm : plantcv.geospatial.images.DSM object
        Canopy height model, from geospatial.subtract_dsm
    geojson : str
        Path to the shape file containing the regions for analysis
    bins : int
        Number of bins for height distribution (default = 10).
    label : str, list, optional
        Optional label parameter, modifies the variable name of observations
        recorded (default = pcv.params.sample_label).

    """
    # Set label to params.sample_label if None
    if label is None:
        label = params.sample_label
    # DSM tifs contain just one band of data, so make the array 2D
    dsm_data = dsm[:, :, 0]

    # Set nodata value
    nodata_value = -999
    if dsm.nodata is not None:
        nodata_value = dsm.nodata

    # Gather plot IDs from the geojson
    ids = _gather_ids(geojson=geojson)

    # Calculate range of histogram
    # First replace any nans so they do not affect range calculation
    dsm[np.isnan(dsm)] = nodata_value
    filtered = dsm[dsm != nodata_value]
    histrange = (filtered.min(), filtered.max())

    # Use raster stats to calculate distribution
    height_values = zonal_stats(geojson, dsm_data,
                                affine=dsm.transform,
                                nodata=nodata_value, stats=['mean', 'std'],
                                add_stats={'histogram': lambda x: _histogram_stats(x, bins=bins, histrange=histrange)})

    # For debug graph
    height_means = []

    # Output values
    for i, id in enumerate(ids):
        j = height_values[i]
        # Add height to debug
        height_means.append(j["mean"])

        observation_sample = label + "_" + str(id)
        outputs.add_observation(sample=observation_sample,
                                variable='height_frequencies',
                                trait='height frequencies',
                                method='plantcv-geospatial.analyze.chm',
                                scale='frequency', datatype=list,
                                value=j["histogram"]["counts"], label=j["histogram"]["bin_edges"])
        outputs.add_observation(sample=observation_sample,
                                variable='height_mean',
                                trait='height mean',
                                method='plantcv-geospatial.analyze.chm',
                                scale='units', datatype=float,
                                value=j["mean"], label='none')
        outputs.add_observation(sample=observation_sample,
                                variable='height_std',
                                trait='height standard deviation',
                                method='plantcv-geospatial.analyze.chm',
                                scale='units', datatype=float,
                                value=j["std"], label='none')

    df = pd.DataFrame({'value': height_means})
    height_chart = alt.Chart(df).mark_bar().encode(x=alt.X('value', bin=True, title='Mean Plot Height'),
                                                   y=alt.Y('count()', title='Frequency'))

    _debug(visual=height_chart, filename=os.path.join(params.debug_outdir, label + '_plot_height_mean.png'))
    return height_chart
