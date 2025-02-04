#
from shapely.geometry import LineString, Polygon, mapping
from plantcv.geospatial._helpers import _unpack_point_shapefiles
import fiona


def create_grid_cells(four_points_path, plot_geojson_path, out_path,
                      horizontal_cells=8, vertical_length=3.6576, horizontal_length=0.9144):
    """Create a grid of cells from input shapefiles and save them to a new shapefile.

    Parameters:
    -----------
    four_points_path : str
        Path to geojson containing four corner points
    plot_geojson_path : str
        Path to geojson containing plot corner points
    out_path : str
        Path where the output grid cells geojson will be saved
    horizontal_cells : int, optional
        Number of cells to divide the horizontal edge into (default: 8)
    vertical_length : float, optional
        Height of each grid cell (default: 3.6576m )
    horizontal_length : float, optional
        Width of each grid cell (default: 0.9144m )

    Returns:
    --------
    list
        List of dictionaries containing the created grid cell polygons
    """
    # Read the four corner points shapefile
    with fiona.open(four_points_path, 'r') as shapefile:
        # Unpack coordinates regardless of Multi-Point or Point geometry type
        coordinates = _unpack_point_shapefiles(shapefile)
        crs = shapefile.crs
        driver = shapefile.driver
        schema = {
            'geometry': 'Polygon',
            'properties': {}
        }

    # Read the plot boundaries shapefile
    with fiona.open(plot_geojson_path, 'r') as shapefile:
        plot_corner_points = _unpack_point_shapefiles(shapefile)

    # Create LineString objects for edges
    # NOTE: order will depend on order that 4 corners are clicked in
    edge_1 = LineString([coordinates[1][0], coordinates[2][0]])  # vertical edge
    edge_2 = LineString([coordinates[0][0], coordinates[1][0]])  # horizontal edge

    # Calculate direction vectors
    edge_1_dir = ((edge_1.coords[1][0] - edge_1.coords[0][0]) / edge_1.length,
                  (edge_1.coords[1][1] - edge_1.coords[0][1]) / edge_1.length)
    edge_2_dir = ((edge_2.coords[1][0] - edge_2.coords[0][0]) / edge_2.length,
                  (edge_2.coords[1][1] - edge_2.coords[0][1]) / edge_2.length)

    # Cell width
    horizontal_threshold = horizontal_length

    # Initialize list for storing grid cells
    grid_cells = []

    # Create grid cells for each plot
    for points in plot_corner_points:
        for column_number in range(horizontal_cells):
            # Calculate corners of each grid cell
            bottom_left = (points[0][0] + column_number * horizontal_threshold * edge_2_dir[0],
                           points[0][1] + column_number * horizontal_threshold * edge_2_dir[1])

            bottom_right = (bottom_left[0] + horizontal_threshold * edge_2_dir[0],
                            bottom_left[1] + horizontal_threshold * edge_2_dir[1])

            top_left = (bottom_left[0] + vertical_length * edge_1_dir[0],
                        bottom_left[1] + vertical_length * edge_1_dir[1])

            top_right = (bottom_right[0] + vertical_length * edge_1_dir[0],
                         bottom_right[1] + vertical_length * edge_1_dir[1])

            # Create polygon from corners
            cell = Polygon([bottom_left, bottom_right, top_right, top_left, bottom_left])
            grid_cells.append({"polygon": cell})

    # Save grid cells to output shapefile
    with fiona.open(out_path, 'w', driver=driver, crs=crs, schema=schema) as shapefile:
        for cell in grid_cells:
            shapefile.write({
                'geometry': mapping(cell["polygon"])
            })

    return grid_cells


#
from shapely.geometry import LineString, Polygon, mapping
from plantcv.geospatial._helpers import _unpack_point_shapefiles
import fiona


def auto_create_grid_cells(four_points_path, out_path, alley_size, num_ranges, num_plots,
                      row_per_plot=4, vertical_length=3.6576, horizontal_length=0.9144):
    """Create a grid of cells from input shapefiles and save them to a new shapefile.

    Parameters:
    -----------
    four_points_path : str
        Path to geojson containing four corner points
    out_path : str
        Path where the output grid cells geojson will be saved
    alley_size : float
        Size of alley spaces beteen ranges
    num_ranges : int
        Number of ranges (vertical cell rows)
    num_plots : int
        Number of plots (horizontal cell columns) 
    row_per_plot : int, optional
        Number of cells to divide the horizontal edge into (default: 4)
    vertical_length : float, optional
        Height of each grid cell (default: 3.6576m )
    horizontal_length : float, optional
        Width of each grid cell (default: 0.9144m )

    Returns:
    --------
    list
        List of dictionaries containing the created grid cell polygons
    """
    # Read the four corner points shapefile
    with fiona.open(four_points_path, 'r') as shapefile:
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
    edge_1 = LineString([coordinates[1][0], coordinates[2][0]])  # vertical edge
    edge_2 = LineString([coordinates[0][0], coordinates[1][0]])  # horizontal edge

    # Calculate direction vectors
    edge_1_dir = ((edge_1.coords[1][0] - edge_1.coords[0][0]) / edge_1.length,
                  (edge_1.coords[1][1] - edge_1.coords[0][1]) / edge_1.length)
    edge_2_dir = ((edge_2.coords[1][0] - edge_2.coords[0][0]) / edge_2.length,
                  (edge_2.coords[1][1] - edge_2.coords[0][1]) / edge_2.length)

    # Initialize list for storing grid cells
    grid_cells = []

    # Initialize first coordinate of the grid 
    anchor_point = coordinates[0] ## AKA bottom_left
    
    # Create grid cells for each plot
    for range_number in range(num_ranges):
        for column_number in range(num_plots):
            # Calculate corners of each grid cell
            bottom_left = (anchor_point[0][0] + column_number * horizontal_length * edge_2_dir[0],
                           anchor_point[0][1] + column_number * horizontal_length * edge_2_dir[1] +
                           # Include alley spacing in range location 
                           range_number * (vertical_length + alley_size) * edge_1_dir[1])

            bottom_right = (bottom_left[0] + horizontal_length * edge_2_dir[0],
                            bottom_left[1] + horizontal_length * edge_2_dir[1])

            top_left = (bottom_left[0] + vertical_length * edge_1_dir[0],
                        bottom_left[1] + vertical_length * edge_1_dir[1])

            top_right = (bottom_right[0] + vertical_length * edge_1_dir[0],
                         bottom_right[1] + vertical_length * edge_1_dir[1])

            # Create polygon from corners
            cell = Polygon([bottom_left, bottom_right, top_right, top_left, bottom_left])
            grid_cells.append({"polygon": cell})

    # Save grid cells to output shapefile
    with fiona.open(out_path, 'w', driver=driver, crs=crs, schema=schema) as shapefile:
        for cell in grid_cells:
            shapefile.write({
                'geometry': mapping(cell["polygon"])
            })

    return grid_cells
