"""Tests for geospatial.visualize.height_distribution"""

import dill as pickle
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


#def test_height_distribution_plot_debug(test_data):
#    """Test for PlantCV, debug=plot."""
#    params.debug = "plot"
#    # Read in test data
#    with open(test_data.dsm_pickled, "rb") as f:
#        img = pickle.load(f)
#    img.nodata = None
#    chart = height_distribution(img=img, geojson=test_data.multipoly, n=2, seed=1, label="test")
#    assert isinstance(chart, alt.FacetChart)


#def test_height_distribution_more_plots_than_available(test_data):
#    """Test for PlantCV, requesting more plots than exist in the geojson."""
#    params.debug = None
#    # Read in test data
#    with open(test_data.dsm_pickled, "rb") as f:
#        img = pickle.load(f)
#    img.nodata = None
#    chart = height_distribution(img=img, geojson=test_data.poly_crop, n=9, label="test")
#    # Only one region exists in poly_crop, so only one plot ID should appear in the data
#    assert chart.data["plot_id"].nunique() == 1
