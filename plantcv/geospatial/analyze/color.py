# Analyze color over shapefile-defined regions
import cv2
import os
import numpy as np
import pandas as pd
import altair as alt
from plantcv.plantcv import outputs, params
from plantcv.plantcv._debug import _debug
from plantcv.geospatial._helpers import _histogram_stats, _gather_ids
from rasterstats import zonal_stats
from scipy import stats
from functools import partial


def _hue_circ_stats(h):
    """Function to calculate hue circular stats from the h channel of a masked image

    Parameters
    ----------
    h : np.ndarray
        h channel from a masked image

    Returns
    -------
    dict
        dictionary with hue circular mean and standard deviation
    """
    hue_circular_mean = stats.circmean(h[np.where(h > 0)], high=179, low=0) * 2
    hue_circular_std = stats.circstd(h[np.where(h > 0)], high=179, low=0) * 2

    return {
        'hue_circular_mean' : hue_circular_mean,
        'hue_circular_std' : hue_circular_std
    }


def _channel_stats(img, mask, geojson, bins, channels, channel_ids, histrange, ids, label):
    """Uses raster stats to calculate color summary stats and histograms from individual channels

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        Spectral_Data object of geotif data, generated using [read_geotif]
    mask : np.ndarray
        Binary mask with objects of interest segmented
    geojson : str
        Path to a shapefile containing plot boundaries
    bins : int
        Number of bins for the histogram
    channels : list
        List of the single channel arrays to calculate stats
    channel_ids : list
        List of string names for channels
    histrange : tuple
        Min and max of the range for the histogram
    ids : list
        List of string names for ids in geojson, returned from _gather_ids
    label : str
        Label to include as prefix
    """
    for idx, channel in enumerate(channels):
        # Convert to float and fill in no data values required for zonal stats
        channel = channel.astype(np.float32)
        channel[mask == 0] = -999
        color_values = zonal_stats(geojson, channel,
                                   affine=img.metadata["transform"],
                                   nodata=-999, stats=['mean', 'std'],
                                   add_stats={'histogram': lambda x: _histogram_stats(x, bins=bins, histrange=histrange)})
        for i, id in enumerate(ids):
            j = color_values[i]
            observation_sample = label + "_" + str(id)
            outputs.add_observation(sample=observation_sample,
                                    variable=channel_ids[idx] + '_frequencies',
                                    trait=channel_ids[idx]+' frequencies',
                                    method='plantcv-geospatial.analyze.color',
                                    scale='frequency', datatype=list,
                                    value=j["histogram"]["counts"], label=j["histogram"]["bin_edges"])
            outputs.add_observation(sample=observation_sample,
                                    variable=channel_ids[idx] + '_mean',
                                    trait=channel_ids[idx]+' mean',
                                    method='plantcv-geospatial.analyze.color',
                                    scale='none', datatype=float,
                                    value=j["mean"], label='none')
            outputs.add_observation(sample=observation_sample,
                                    variable=channel_ids[idx] + '_std',
                                    trait=channel_ids[idx]+' standard deviation',
                                    method='plantcv-geospatial.analyze.color',
                                    scale='none', datatype=float,
                                    value=j["std"], label='none')


def color(img, bin_mask, geojson, bins=10, colorspaces="hsv", label=None):
    """Analyze color in individual plots from a spectral object using plot boundaries.

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        Spectral_Data object of geotif data, generated using [read_geotif]
    bin_mask : np.ndarray
        Binary mask with objects of interest segmented
    geojson : str
        Path to a shapefile containing plot boundaries
    bins : int
        Number of bins for the histogram, default=10
    colorspaces : str, optional
        Colorspaces to analyze (case-insensitive): "all", "rgb", "lab", or "hsv", by default "hsv"
    label : str, optional
        Optional label for plots, by default None

    Returns
    -------
    plantcv.plantcv.classes.Spectral_data
        The input spectral object.
    """
    # Set label to params.sample_label if None
    if label is None:
        label = params.sample_label

    # Make masked image to convert to other colorspaces
    masked = cv2.bitwise_and(img.pseudo_rgb, img.pseudo_rgb, mask=bin_mask)

    # Always output hue circular stats:

    # Convert the BGR image to HSV
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    # Extract the hue, saturation, and value channels
    h, s, v = cv2.split(hsv)

    h = h.astype(np.float32)
    h[bin_mask == 0] = -999

    ids = _gather_ids(geojson=geojson)

    hcm = []
    hue_stats = zonal_stats(geojson, h,
                            affine=img.metadata["transform"],
                            nodata=-999, stats=['mean'],
                            add_stats={'hue_stats': partial(_hue_circ_stats)})

    for idx, i in enumerate(hue_stats):
        observation_sample = label + "_" + str(ids[idx])
        hcm.append(i["hue_stats"]["hue_circular_mean"])
        outputs.add_observation(sample=observation_sample,
                                variable='hue_circular_mean',
                                trait='hue circular mean', method='plantcv-geospatial.analyze.color',
                                scale='degrees', datatype=float,
                                value=float(i["hue_stats"]["hue_circular_mean"]), label='degrees')
        outputs.add_observation(sample=observation_sample,
                                variable='hue_circular_std',
                                trait='hue circular standard deviation',
                                method='plantcv-geospatial.analyze.color',
                                scale='degrees', datatype=float,
                                value=float(i["hue_stats"]["hue_circular_std"]), label='degrees')

    if colorspaces.upper() in ('RGB', 'ALL'):
        # Extract the blue, green, and red channels
        b, g, r = cv2.split(masked)
        _channel_stats(img, bin_mask, geojson, bins, channels=[b, g, r],
                       channel_ids=["blue", "green", "red"], histrange=(0, 255),
                       ids=ids, label=label)

    if colorspaces.upper() in ('LAB', 'ALL'):
        # Convert the BGR image to LAB
        lmy = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
        # Extract the lightness, green-magenta, and blue-yellow channels
        l, m, y = cv2.split(lmy)
        _channel_stats(img, bin_mask, geojson, bins, channels=[l, m, y],
                       channel_ids=["lightness", "green-magenta", "blue-yellow"],
                       histrange=(0, 255), ids=ids, label=label)

    if colorspaces.upper() in ('HSV', 'ALL'):
        _channel_stats(img, bin_mask, geojson, bins, channels=[h, s, v],
                       channel_ids=["hue", "saturation", "value"], histrange=(0, 255),
                       ids=ids, label=label)

    df = pd.DataFrame({'value': hcm})
    hue_chart = alt.Chart(df).mark_bar().encode(x=alt.X('value', bin=True, title='Hue Circular Mean'),
                                                y=alt.Y('count()', title='Frequency'))

    _debug(visual=hue_chart, filename=os.path.join(params.debug_outdir, label + '_hue_circular_mean.png'))

    return img
