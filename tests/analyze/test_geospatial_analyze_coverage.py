import pytest
import joblib
from plantcv.plantcv import outputs, params
from plantcv.geospatial.analyze import coverage as analyze_coverage


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_coverage(debug, tmpdir, test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    bin_mask = img.array_data[:, :, 2]  # Make a grayscale img to use as the mask
    # Debug mode
    params.debug = debug
    _ = analyze_coverage(img=img, bin_mask=bin_mask, geojson=test_data.square_crop)
    assert outputs.observations["default_0"]["percent_coverage"]["value"] <= 1


def test_coverage_with_geo_ids(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    bin_mask = img.array_data[:, :, 2]  # Make a grayscale img to use as the mask
    _ = analyze_coverage(img=img, bin_mask=bin_mask, geojson=test_data.geojson_with_id)
    assert outputs.observations["888"]["percent_coverage"]["value"] <= 1
