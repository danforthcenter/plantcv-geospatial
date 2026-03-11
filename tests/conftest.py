import os
import pytest
import matplotlib

# Disable plotting
matplotlib.use("Template")

class TestData:
    def __init__(self):
        """Initialize testing variables in TestData class.

        Attributes:
        -----------
        datadir            : str
            path to test data directory
        cropped_tif        : str
            615.tif file
            Used for testing read_geotif
        multi_pickled      : str
            multi_img.spectral file
            Contains a pickled 5-band plantcv.Spectral_data object
            Used for testing analyze.spectral_index and analyze.height_subtraction
        empty_tif          : str
            cropped_empty.tif file
            Used for testing read_geotif
        rgb_tif            : str
            rgb.tif file
            Used for testing read_geotif
        rbg_uint16_tif     : str
            rgb_uint16.tif file
            Used for testing read_geotif
        rgb_pickled        : str
            rgb_img.spectral file
            Contains a pickled plantcv.Spectral_data object
            Used for testing center_grid_rois, points_to_geojson, transform_points,
            points2roicircle, _helpers, transform_polygons, create_shapes.napari_grid, shapes_to_geojson,
            create_shapes.grid, create_shapes.grid_from_coords, analyze.height_percentile, analyze.coverage,
            analyze.height_subtraction
        pts_geojson        : str
            test_pts.geojson file
            Used for testing transform_points and points_to_roi_circle
        single_pts_geojson : str
            single_test_pts.geojson file
            Used for testing transform_points
        square_crop        : str
            square_crop.geojson file, a square shape.
            Used for testing analyze.coverage, analyze.height_percentile, and read_geotif.
        geojson_with_id   : str
            square_crop_with_id.geojson file
            contains "ID" in properties and is otherwise identical to square_crop attribute file
            Used for testing analyze.height_percentile and analyze.coverage
        geojson_with_fid   : str
            square_crop_with_fid.geojson file,
            contains "FID" in properties and is otherwise identical to square_crop attribute file
            Used for testing analyze.height_percentile
        point_crop         : str
            point_crop.geojson  file
            Used for testing read_geotif, create_shapes.grid and create_shapes.grid_from_coords
        multipolygon       : str
            multipolygon_fortests.geojson file
            Used for testing transform.polygons and analyze.spectral_index
        epsg4326_geojson   : str
            epsg4326points.geojson file
            Used for testing _helpers._transform_geojson_crs
        plot_bounds        : str
            docs_four_points.geojson file
            Used for testing create_shapes.grid_from_coords
        plot_points        : str
            plot_points.geojson file
            Used for testing create_shapes.grid_from_coords
        test_netcdf        : str
            subset_test.nc file
            Used for testing read_netcdf
        netcdf_testcrop    : str
            netcdf_test.geojson file
            Used for testing read_netcdf
        gray_tif           : str
            gray.tif file
            Used for testing read_geotif
        """
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        # multispectral image
        self.cropped_tif = os.path.join(self.datadir, "615.tif")
        # multispectral pickled
        self.multi_pickled = os.path.join(self.datadir, "multi_img.spectral")
        # empty image
        self.empty_tif = os.path.join(self.datadir, "cropped_empty.tif")
        # rgb image
        self.rgb_tif = os.path.join(self.datadir, "rgb.tif")
        # rgb uint16 image
        self.rgb_uint16_tif = os.path.join(self.datadir, "rgb_uint16.tif")
        # rgb pickled
        self.rgb_pickled = os.path.join(self.datadir, "rgb_img.spectral")
        # multiPoints shapefilex
        self.pts_geojson = os.path.join(self.datadir, "test_pts.geojson")
        # points shapefilex
        self.single_pts_geojson = os.path.join(self.datadir, "single_test_pts.geojson")
        # polygon shapefile
        self.square_crop = os.path.join(self.datadir, "square_crop.geojson")
        # polygon shapefile with "ID" in properties
        self.geojson_with_id = os.path.join(self.datadir, "square_crop_with_id.geojson")
        # polygon shapefile with "FID" in properties
        self.geojson_with_fid = os.path.join(self.datadir, "square_crop_with_fid.geojson")
        # polygon shapefile with "PlotName" in properties
        self.square_crop_with_plotname = os.path.join(self.datadir, "square_crop_with_plotname.geojson")
        # polygon shapefile with "plot_ids" in properties
        self.square_crop_with_plot_ids = os.path.join(self.datadir, "square_crop_with_plot_ids.geojson")
        # points shapefile
        self.point_crop = os.path.join(self.datadir, "point_crop.geojson")
        # multi polygon shapefile
        self.multipolygon = os.path.join(self.datadir, "multipolygon_fortests.geojson")
        # epsg4326 points shapefile
        self.epsg4326_geojson = os.path.join(self.datadir, "epsg4326points.geojson")
        # plot bounds shapefile
        self.plot_bounds = os.path.join(self.datadir, "docs_four_points.geojson")
        # plot points shapefile
        self.plot_points = os.path.join(self.datadir, "plot_points.geojson")
        # read netcdf example file and cropping shapefile
        self.test_netcdf = os.path.join(self.datadir, "subset_test.nc")
        self.netcdf_testcrop = os.path.join(self.datadir, "netcdf_test.geojson")
        # DEM for grayscale tif reading
        self.gray_tif = os.path.join(self.datadir, "gray.tif")

@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV-geospatial package."""
    return TestData()
