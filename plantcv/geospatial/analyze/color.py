# Analyze color over shapefile-defined regions
import cv2
import os
import numpy as np
from plantcv.plantcv import outputs, params
from plantcv.plantcv._debug import _debug
from plantcv.geospatial._helpers import _histogram_stats
from rasterstats import zonal_stats
from scipy import stats

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

def _channel_stats(img, mask, geojson, bins, label, channels, ids, histrange):
    """Uses raster stats to calculate color summary stats and histograms from individual channels

    Parameters
    ----------
    img : [spectral_object]
        Spectral_Data object of geotif data, generated using [read_geotif]
    mask : np.ndarray
        Binary mask with objects of interest segmented
    geojson : str
        Path to a shapefile containing plot boundaries
    bins : int
        Number of bins for the histogram
    label : str
        Optional label for numbered plots
    channels : list
        List of the single channel arrays to calculate stats
    ids : list
        List of string names for channels
    histrange : tuple
        Min and max of the range for the histogram
    """
    for idx, i in enumerate(channels):
        # Convert to float and fill in no data values required for zonal stats
        i = i.astype(np.float32)
        i[mask == 0] = -999
        color_values = zonal_stats(geojson, i,
                        affine=img.metadata["transform"],
                        nodata=-999, stats=['mean', 'std'],
                        add_stats={'histogram': lambda x: _histogram_stats(x, bins=bins, histrange=histrange)})
        for jdx, j in enumerate(color_values):
            outputs.add_observation(sample=label+'_'+str(jdx), variable=ids[idx] + '_frequencies', 
                                    trait=ids[idx]+' frequencies',method='plantcv.geospatial.analyze.color', 
                                    scale='frequency', datatype=list,
                                    value=j["histogram"]["counts"], label=j["histogram"]["bin_edges"])
            outputs.add_observation(sample=label+'_'+str(jdx), variable=ids[idx] + '_mean', 
                                    trait=ids[idx]+' mean',method='plantcv.geospatial.analyze.color', 
                                    scale='none', datatype=float,
                                    value=j["mean"], label='none')
            outputs.add_observation(sample=label+'_'+str(jdx), variable=ids[idx] + '_std', 
                                    trait=ids[idx]+' standard deviation',method='plantcv.geospatial.analyze.color', 
                                    scale='none', datatype=float,
                                    value=j["std"], label='none')
    return


def color(img, mask, geojson, bins=10, colorspaces="hsv", label=None):
    """Analyze color in individual plots from a spectral object using plot boundaries.

    Parameters
    ----------
    img : [spectral_object]
        Spectral_Data object of geotif data, generated using [read_geotif]
    mask : np.ndarray
        Binary mask with objects of interest segmented
    geojson : str
        Path to a shapefile containing plot boundaries
    bins : int
        Number of bins for the histogram, default=10
    label : str, optional
        Optional label for numbered plots
    colorspaces : str, optional
        Colorspaces to analyze, "all", "rgb", "lab", or "hsv", by default "hsv"
    label : str, optional
        Optional label for plots, by default None

    Returns
    -------
    [spectral_object]
        The input spectral object. 
    """
    if not label:
        label = "plot"
        
    # Make masked image to convert to other colorspaces
    masked = cv2.bitwise_and(img.pseudo_rgb, img.pseudo_rgb, mask=mask)

    # Always output hue circular stats:
    
    # Convert the BGR image to HSV
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    # Extract the hue, saturation, and value channels
    h, s, v = cv2.split(hsv)
    
    h = h.astype(np.float32)
    h[mask == 0] = -999
    hue_stats = zonal_stats(geojson, h,
                        affine=img.metadata["transform"],
                        nodata=-999, stats=['mean'],
                        add_stats={'hue_stats': lambda x: _hue_circ_stats(x)})
    
    for idx, i in enumerate(hue_stats):
        outputs.add_observation(sample=label+'_'+str(idx), variable='hue_circular_mean', 
                                    trait='hue circular mean',method='plantcv.geospatial.analyze.color', 
                                    scale='degrees', datatype=float,
                                    value=float(i["hue_stats"]["hue_circular_mean"]), label='degrees')
        outputs.add_observation(sample=label+'_'+str(idx), variable='hue_circular_std', 
                                    trait='hue circular standard deviation',
                                    method='plantcv.geospatial.analyze.color', 
                                    scale='degrees', datatype=float,
                                    value=float(i["hue_stats"]["hue_circular_std"]), label='degrees')
    
    if colorspaces.upper() in ('RGB', 'ALL'):
        # Extract the blue, green, and red channels
        b, g, r = cv2.split(masked)
        _channel_stats(img, mask, geojson, bins, label, channels=[b, g, r], ids=["b", "g", "r"], histrange=(0,255))
        
    if colorspaces.upper() in ('LAB', 'ALL'):
         # Convert the BGR image to LAB
        lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
        # Extract the lightness, green-magenta, and blue-yellow channels
        l, a, b = cv2.split(lab)
        _channel_stats(img, mask, geojson, bins, label, channels=[l], ids=["l"], histrange=(0,100))
        _channel_stats(img, mask, geojson, bins, label, channels=[a, b], ids=["a", "b"], histrange=(-128, 127))
        
    if colorspaces.upper() in ('HSV', 'ALL'):
        _channel_stats(img, mask, geojson, bins, label, channels=[h], ids=["h"], histrange=(0,359))
        _channel_stats(img, mask, geojson, bins, label, channels=[s, v], ids=["s", "v"], histrange=(0,100))

    hue_chart = outputs.plot_dists(variable="hue_circular_mean")
    _debug(visual=hue_chart, filename=os.path.join(params.debug_outdir, label + '_hue_ciruclar_mean.png'))

    return img