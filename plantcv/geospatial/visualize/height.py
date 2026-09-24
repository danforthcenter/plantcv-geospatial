# Visualize height distributions for a random subset of plots
import os
import numpy as np
import pandas as pd
import altair as alt
import geopandas
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.geospatial._helpers import _gather_ids, _histogram_stats
from rasterstats import zonal_stats


def height_distribution(img, geojson, n=9, bins=50, lower=25, upper=90, seed=None, label=None):
    """
    Plot height histograms for a random subset of plots.

    Intended to help choose lower/upper percentile cutoffs for
    plantcv.geospatial.analyze.height_percentile by showing where those
    percentiles fall relative to the height distribution (e.g. soil vs.
    canopy elevation) within a set of randomly selected plots.

    Parameters
    ----------
    img : plantcv.geospatial.images.DSM object
        Single-band geospatial raster data, generally from read.geotif
    geojson : str
        Path to the shape file containing the regions to sample from
    n : int, optional
        Number of plots to randomly sample (default = 9). If the geojson
        contains fewer regions than n, all regions are used.
    bins : int, optional
        Number of histogram bins (default = 50)
    lower : int, optional
        Lower percentile cutoff to mark on each histogram (default = 25)
    upper : int, optional
        Upper percentile cutoff to mark on each histogram (default = 90)
    seed : int, optional
        Random seed, for reproducible plot sampling (default = None)
    label : str, optional
        Optional label used in the debug output filename
        (default = pcv.params.sample_label)

    Returns
    -------
    alt.FacetChart
        Grid of height histograms, one per sampled plot
    """
    if label is None:
        label = params.sample_label

    # Raster data is single-band, cast to float to avoid overflow in zonal stats
    raster_data = img[:, :, 0].astype(np.float32)
    nodata_value = img.nodata if img.nodata is not None else -999

    # Gather plot IDs (matches the same ID logic used by analyze.height_percentile)
    ids = _gather_ids(geojson=geojson)
    regions = geopandas.read_file(geojson)

    # Randomly sample n plots (or all of them if fewer than n exist)
    n = min(n, len(regions))
    rng = np.random.default_rng(seed)
    sample_idx = np.sort(rng.choice(len(regions), size=n, replace=False))
    sample = regions.iloc[sample_idx]
    sample_ids = [str(ids[i]) for i in sample_idx]

    # Pull the raw height values contained within each sampled plot
    zstats = zonal_stats(sample, raster_data, affine=img.transform,
                         nodata=nodata_value, stats=[], raster_out=True)

    # Bin each plot's values independently
    records = []
    for plot_id, zstat in zip(sample_ids, zstats):
        values = zstat["mini_raster_array"].compressed()
        if values.size > 0:
            hist = _histogram_stats(values, bins=bins, histrange=(values.min(), values.max()))
            records.extend({"plot_id": plot_id, "kind": "bin", "bin_start": hist["bin_edges"][i],
                            "bin_end": hist["bin_edges"][i + 1], "count": hist["counts"][i],
                            "value": None, "percentile": None}
                           for i in range(len(hist["counts"])))
            records.append({"plot_id": plot_id, "kind": "percentile", "bin_start": None, "bin_end": None,
                            "count": None, "value": float(np.percentile(values, lower)),
                            "percentile": str(lower) + "th"})
            records.append({"plot_id": plot_id, "kind": "percentile", "bin_start": None, "bin_end": None,
                            "count": None, "value": float(np.percentile(values, upper)),
                            "percentile": str(upper) + "th"})
    df = pd.DataFrame(records)

    histogram = alt.Chart().transform_filter(alt.datum.kind == "bin").mark_bar(color="gray").encode(
        x=alt.X("bin_start:Q", title="Height", scale=alt.Scale(zero=False)), x2="bin_end:Q",
        y=alt.Y("count:Q", title="Frequency"), y2=alt.Y2(datum=0))

    percentile_lines = alt.Chart().transform_filter(alt.datum.kind == "percentile").mark_rule(
        strokeDash=[8, 4], strokeWidth=3).encode(x=alt.X("value:Q", scale=alt.Scale(zero=False)),
                                                 color=alt.Color("percentile:N", title="Percentile"))

    ncols = int(np.ceil(np.sqrt(n)))
    height_chart = alt.layer(histogram, percentile_lines, data=df).facet(
        facet=alt.Facet("plot_id:N", title="Plot"), columns=ncols).resolve_scale(x="independent", y="independent")

    _debug(visual=height_chart, filename=os.path.join(params.debug_outdir, label + "_height_distribution.png"))

    return height_chart
