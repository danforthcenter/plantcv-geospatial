"""Tests for geospatial.visualize.height_distribution"""

import dill as pickle
import pytest
import altair as alt
from plantcv.plantcv import params
from plantcv.geospatial.visualize import height_distribution

@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_height_distribution(debug, tmpdir, test_data):
    """Test for PlantCV."""
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    # Read in test data
    with open(test_data.dsm_pickled, "rb") as f:
        img = pickle.load(f)
    img.nodata = 0
    # Debug mode
    params.debug = debug
    chart = height_distribution(img=img, geojson=test_data.multipoly, n=2, seed=1)
    assert isinstance(chart, alt.FacetChart)
