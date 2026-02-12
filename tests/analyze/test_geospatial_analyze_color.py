import joblib
from plantcv.plantcv import outputs
from plantcv.geospatial.analyze import color as analyze_color


def test_coverage(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    bin_mask = img.array_data[:, :, 2]  # Make a grayscale img to use as the mask
    _ = analyze_color(img=img, bin_mask=bin_mask, geojson=test_data.square_crop)
    assert round(outputs.observations["default_1"]["hue_circular_mean"]["value"]) == 41