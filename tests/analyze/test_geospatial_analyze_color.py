import dill as pickle
from plantcv.plantcv import outputs
from plantcv.geospatial.analyze import color as analyze_color


def test_analyze_color(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    bin_mask = img.array_data[:, :, 2]  # Make a grayscale img to use as the mask
    _ = analyze_color(img=img, bin_mask=bin_mask, geojson=test_data.poly_crop, colorspaces="all")
    assert round(outputs.observations["default_888"]["hue_circular_mean"]["value"]) == 41
    assert outputs.observations["default_888"]["hue_frequencies"]["value"][0] == 4497


def test_analyze_color_with_geo_ids(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    bin_mask = img.array_data[:, :, 2]  # Make a grayscale img to use as the mask
    _ = analyze_color(img=img, bin_mask=bin_mask, geojson=test_data.geojson_with_id)
    assert round(outputs.observations["default_888"]["hue_circular_mean"]["value"]) == 41
    assert outputs.observations["default_888"]["hue_frequencies"]["value"][0] == 4497
