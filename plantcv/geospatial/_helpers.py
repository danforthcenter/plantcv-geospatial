# PlantCV-geospatial helper functions
from shapely.geometry import LineString, Polygon
from rasterio.plot import plotting_extent
from matplotlib import pyplot as plt
from plantcv.plantcv import params
import geopandas
import fiona
import cv2
import os


def _transform_geojson_crs(img, geojson):
    """
    Helper function for opening and transforming Coordinate System
    of a geojson/shapefile

    Keyword inputs:
    Inputs:
    img:        A spectral object from read_geotif.
    geojson:    Path to the shapefile.

    :param img: [spectral object]
    :return geojson: str
    :return gdf: geopandas
    """
    gdf = geopandas.read_file(geojson)

    img_crs = img.metadata['crs']

    # Check spectral object and geojson have the same CRS, if not then convert
    if not gdf.crs == img_crs:
        gdf = gdf.to_crs(crs=img_crs)

    return gdf


def _unpack_point_shapefiles(shapefile):
    """
    Helper function for opening and unpacking Point and Multi-Point type shapefile data

    Keyword inputs:
    Inputs:
    shapefile: Fiona formatted shapefile data

    :param shapefile: class 'fiona.collection.Collection'
    :return coordinates: list
    """
    if type(shapefile[0]['geometry']['coordinates']) is list:
        coordinates = [shape['geometry']['coordinates'] for shape in shapefile]
    if type(shapefile[0]['geometry']['coordinates']) is tuple:
        coordinates = [[shape['geometry']['coordinates']] for shape in shapefile]
    return coordinates


def _calc_direction_vectors(plot_bounds):
    """
    Helper function for opening plot boundaries and calculating direction vectors

    Keyword inputs:
    Inputs:
    plot_bounds: path to Fiona formatted shapefile data of the plot boundary

    Returns:
    --------
    horizontal_dir
        Direction vector in the horizontal direction
    vertical_dir
        Direction vector in the vertical direction
    anchor_point
        First coordinate in the boundary shapefile

    :param plot_bounds: str
    :return horizontal_dir: list
    :return vertical_dir: list
    :return anchor_point: tuple
    """
    # Read the four corner points shapefile
    with fiona.open(plot_bounds, 'r') as shapefile:
        # Unpack coordinates regardless of Multi-Point or Point geometry type
        coordinates = _unpack_point_shapefiles(shapefile)
        crs = shapefile.crs
        driver = shapefile.driver
        schema = {
            'geometry': 'Polygon',
            'properties': {}
        }

    # Create LineString objects for edges
    # NOTE: order will depend on order that 4 corners are clicked in
    edge_1 = LineString([coordinates[1][0], coordinates[2][0]])
    edge_2 = LineString([coordinates[0][0], coordinates[1][0]])

    # Calculate direction vectors
    vertical_dir = ((edge_1.coords[1][0] - edge_1.coords[0][0]) / edge_1.length,
                    (edge_1.coords[1][1] - edge_1.coords[0][1]) / edge_1.length)
    horizontal_dir = ((edge_2.coords[1][0] - edge_2.coords[0][0]) / edge_2.length,
                      (edge_2.coords[1][1] - edge_2.coords[0][1]) / edge_2.length)
    anchor_point = coordinates[0]

    return horizontal_dir, vertical_dir, anchor_point, crs, driver, schema


def _calc_plot_corners(anchor_point, horizontal_dir, vertical_dir, col_num,
                       range_num=0, range_length=3.6576, column_length=0.9144,
                       range_spacing=0, column_spacing=0):
    """Create a rectangular/parallelogram polygon

    Parameters:
    -----------
    anchor_point : list
        Path to geojson containing four corner points
    horizontal_dir : tuple
        Horizontal direction vector
    vertical_dir: tuple
        Vertical direction vector
    horizontal_length : float
        Length of the plot in the horizontal dimension
    vertical_length : float
        Length of the plot in the vertical dimension
    alley_size : float
        Length of the alley between plots (vertical dimension)
    col_num : int
        Current column number
    range_num : int
        Current range number

    Returns:
    --------
    list
        List of polygon points
    """
    # Calculate corners of each grid cell, starting with bottom_left
    p1 = (anchor_point[0][0] + col_num * (column_length + column_spacing) * horizontal_dir[0],
          anchor_point[0][1] + range_num * (range_length + range_spacing) * vertical_dir[1])

    p2 = (p1[0] + column_length * horizontal_dir[0],  # bottom_right
          p1[1] + column_length * horizontal_dir[1])

    p3 = (p1[0] + range_length * vertical_dir[0],  # top_left
          p1[1] + range_length * vertical_dir[1])

    p4 = (p2[0] + range_length * vertical_dir[0],  # top_right
          p2[1] + range_length * vertical_dir[1])

    return p1, p2, p3, p4


def _split_subplots(polygon, num_divisions):
    """Split a polygon into equidistant subplots

    Parameters:
    -----------
    polygon : list
        Fiona formatted shapefile data
    row_per_plot : int
        Number of subplots to get divided

    Returns:
    --------
    list
        List of polygon points
    """
    minx, miny, maxx, maxy = polygon.bounds
    division_width = (maxx - minx) / num_divisions
    division_lines = [LineString([(minx + i * division_width, miny),
                                  (minx + i * division_width, maxy)]) for i in range(1, num_divisions)]

    divided_plots = []
    for i in range(num_divisions):
        if i == 0:
            left_boundary = polygon.bounds[0]
        else:
            left_boundary = division_lines[i - 1].coords[0][0]

        if i == num_divisions - 1:
            right_boundary = polygon.bounds[2]
        else:
            right_boundary = division_lines[i].coords[0][0]

        dividing_polygon = Polygon([(left_boundary, miny), (left_boundary, maxy),
                                    (right_boundary, maxy), (right_boundary, miny)])

        divided_plots.append(polygon.intersection(dividing_polygon))

    return divided_plots


def _show_geojson(img, geojson):
    """Split a polygon into equidistant subplots

    Parameters:
    -----------
    img : [spectral_object]
        Spectral_Data object of geotif data, used for plotting
    geojson : str
        Path to the shape file containing the regions

    Returns:
    --------
    list
        List of polygon points
    """
    bounds = geopandas.read_file(geojson)

    # Plot the GeoTIFF
    # Make a flipped image for graphing
    flipped = cv2.merge((img.pseudo_rgb[:, :, [2]],
                         img.pseudo_rgb[:, :, [1]],
                         img.pseudo_rgb[:, :, [0]]))

    _, ax = plt.subplots(figsize=(10, 10))
    fig_extent = plotting_extent(img.array_data[:, :, :3],
                                 img.metadata['transform'])
    ax.imshow(flipped, extent=fig_extent)
    # Plot the shapefile
    bounds.boundary.plot(ax=ax, color="red")
    # Set plot title and labels
    plt.title("GeoJSON shapes on GeoTIFF")
    # Store the plot
    plotting_img = plt.gcf()

    # Print or plot if debug is turned on
    if params.debug is not None:
        if params.debug == 'print':
            plt.savefig(os.path.join(params.debug_outdir, str(
                params.device) + '_shapes_plot.png'), dpi=params.dpi)
            plt.close()
        elif params.debug == 'plot':
            # Use non-blocking mode in case the function is run more than once
            plt.show(block=False)
    else:
        plt.close()

    return plotting_img
