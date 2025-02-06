# Create rectangular geojsons

from shapely.geometry import LineString, Polygon, mapping
from plantcv.geospatial._helpers import _calc_plot_corners, _unpack_point_shapefiles, _calc_direction_vectors
import fiona


def create_polygons(four_points_path, plot_geojson_path, out_path,
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
    # Calculate direction vectors based on plot boundaries
    horizontal_dir, vertical_dir, _, crs, driver, schema = _calc_direction_vectors(
        plot_bounds=four_points_path)
    # Read the plot boundaries shapefile
    with fiona.open(plot_geojson_path, 'r') as shapefile:
        plot_corner_points = _unpack_point_shapefiles(shapefile)

    # Initialize list for storing grid cells
    grid_cells = []

    # Create grid cells for each plot
    for points in plot_corner_points:
        for column_number in range(horizontal_cells):
            anchor_point = points
            p1, p2, p3, p4 =_calc_plot_corners(anchor_point, horizontal_dir, vertical_dir,
                                               horizontal_length, vertical_length, alley_size=0,
                                               col_num=column_number)

            # Create polygon from corners
            cell = Polygon([p1, p2, p4, p3, p1])
            grid_cells.append({"polygon": cell})

    # Save grid cells to output shapefile
    with fiona.open(out_path, 'w', driver=driver, crs=crs, schema=schema) as shapefile:
        for cell in grid_cells:
            shapefile.write({
                'geometry': mapping(cell["polygon"])
            })

    return grid_cells


def create_grid_cells(four_points_path, out_path, alley_size, num_ranges, num_plots,
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
    # Calculate direction vectors based on plot boundaries
    horizontal_dir, vertical_dir, anchor_point, crs, driver, schema = _calc_direction_vectors(
        plot_bounds=four_points_path)

    # Initialize list for storing grid cells
    grid_cells = []

    # Create grid cells for each plot
    for range_number in range(num_ranges):
        for column_number in range(num_plots):
            p1, p2, p3, p4 = _calc_plot_corners(anchor_point, horizontal_dir, vertical_dir,
                                                horizontal_length, vertical_length, alley_size=alley_size,
                                                col_num=column_number, range_num=range_number)

            # Create polygon from corners
            cell = Polygon([p1, p2, p4, p3, p1])
            grid_cells.append({"polygon": cell})

    # Save grid cells to output shapefile
    with fiona.open(out_path, 'w', driver=driver, crs=crs, schema=schema) as shapefile:
        for cell in grid_cells:
            shapefile.write({
                'geometry': mapping(cell["polygon"])
            })

    return grid_cells
