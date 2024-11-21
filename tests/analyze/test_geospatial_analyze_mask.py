import numpy as np
from plantcv.plantcv import outputs
from plantcv.geospatial.analyze import mask as analyze_mask
from plantcv.geospatial import read_geotif


def test_mask(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    bin_mask = img.array_data[:, :, 2]  # Make a grayscale img to use as the mask
    _ = analyze_mask(img=img, bin_mask=bin_mask, geojson=test_data.square_crop)
    assert outputs.observations["default_0"]["percent_coverage"]["value"] <= 1
