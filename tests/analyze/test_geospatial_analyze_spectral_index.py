import pytest
import joblib
from plantcv.plantcv import outputs, params
from plantcv.geospatial.analyze import spectral_index as analyze_spectral


def test_analyze_spectral(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = joblib.load(test_data.multi_pickled)
    img.metadata['nodata'] = 0
    img.array_data = img.array_data[:, :, 2]  # Make a grayscale img to use as the mask

    _ = analyze_spectral(img=img, geojson=test_data.multipolygon)
    assert outputs.observations["default_0"]["percentile_75_datacube"]["value"] <= 1
