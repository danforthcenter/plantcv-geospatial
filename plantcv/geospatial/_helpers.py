# PlantCV-geospatial helper functions
from shapely.geometry import LineString
from rasterio.plot import plotting_extent
from matplotlib import pyplot as plt
from plantcv.plantcv import params
from plantcv.plantcv.fatal_error import fatal_error
import numpy as np
import geopandas
import fiona
import cv2
import os


def _histogram_stats(masked_array, bins, histrange):
    """Helper function to calculate a histogram from a masked array

    Parameters
    ----------
    masked_array : np.ndarray
        Single channel from a masked image
    bins : int
        Number of bins in the output histogram
    histrange : tuple
        Range for the histogram, format (min, max)

    Returns
    -------
    dict
        Dictionary of counts and bin edges
    """
    counts, bin_edges = np.histogram(masked_array, bins, range=histrange)

    return {
        'counts': counts.tolist(),
        'bin_edges': bin_edges.tolist()
    }


def _transform_geojson_crs(img, geojson):
    """
    Helper function for converting the CRS of a geojson to that of a
    corresponding image.

    Parameters:
    -----------
    geojson : str
        Path to the shapefile.
    img : plantcv.geospatial.images.GEO object
        A GEO image object returned by ``read_geotif``.

    Returns:
    --------
    gdf     : geopandas.GeoDataFrame
    """
    gdf = geopandas.read_file(geojson)

    # Check spectral object and geojson have the same CRS, if not then convert
    if not gdf.crs == img.crs:
        gdf = gdf.to_crs(crs=img.crs)

    return gdf


def _unpack_point_shapefiles(shapefile):
    """
    Helper function for opening and unpacking Point and Multi-Point type shapefile data

    Parameters:
    -----------
    shapefile : fiona.collection.Collection
        Fiona formatted shapefile data

    Returns:
    --------
    coordinates : list
        coordinates from shapefile
    """
    if type(shapefile[0]['geometry']['coordinates']) is list:
        coordinates = [shape['geometry']['coordinates'] for shape in shapefile]
    if type(shapefile[0]['geometry']['coordinates']) is tuple:
        coordinates = [[shape['geometry']['coordinates']] for shape in shapefile]
    return coordinates


def _calc_direction_vectors(plot_bounds):
    """
    Helper function for opening plot boundaries and calculating direction vectors

    Parameters
    ----------
    plot_bounds: str
        Path to Fiona formatted shapefile data of the plot boundary

    Returns
    --------
    horizontal_dir : list
        Direction vector in the horizontal direction
    vertical_dir : list
        Direction vector in the vertical direction
    anchor_point : tuple
        First coordinate in the boundary shapefile
    crs : dict
        crs attribute from the plot boundary shapefile
    driver : str
        OGR format driver used to open the plot boundary shapefile
    schema : dict
        plot boundary shapefile schema giving geometry and properties
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
                       range_num=0, range_length=3.6576, row_length=0.9144,
                       range_spacing=0, column_spacing=0, row_num=0, col_length=0):
    """
    Helper function to create a rectangular/parallelogram polygon

    Parameters:
    -----------
    anchor_point : list
        list containing one X, Y coordinate point
    horizontal_dir : tuple
        Horizontal direction vector
    vertical_dir: tuple
        Vertical direction vector
    col_num : int
        Current column number
    range_num : int, optional
        Current range number, defaults to 0.
    range_length : float, optional
        Length of the plot in the horizontal dimension, defaults to 3.6576
    row_length : float, optional
        Length of the plot in the vertical dimension, defaults to 0.9144
    range_spacing : int or float, optional
        Length of spacing between horizontal boundaries, defaults to 0
    column_spacing : int or float, optional
        Length of spacing between vertical boundaries, defaults to 0
    row_num : int, optional
        Number of Rows, defaults to 0
    col_length : int, optional
        Length of columns, defaults to 0

    Returns:
    --------
    p1, p2, p3, p4
        X,Y polygon points. Order is bottom left, bottom right, top left, top right.
    """
    # Calculate corners of each grid cell, starting with bottom_left
    p1 = (anchor_point[0][0] +
          ((col_num * (column_spacing + col_length)) + (row_num * row_length)) * horizontal_dir[0] +
          (range_num * (range_spacing + range_length)) * vertical_dir[0],
          anchor_point[0][1] +
          ((col_num * (column_spacing + col_length)) + (row_num * row_length)) * horizontal_dir[1] +
          ((range_num * (range_spacing + range_length)) * vertical_dir[1])
          )  # bottom_left
    p2 = (p1[0] + row_length * horizontal_dir[0],  # bottom_right
          p1[1] + row_length * horizontal_dir[1])

    p3 = (p1[0] + range_length * vertical_dir[0],  # top_left
          p1[1] + range_length * vertical_dir[1])

    p4 = (p2[0] + range_length * vertical_dir[0],  # top_right
          p2[1] + range_length * vertical_dir[1])

    return p1, p2, p3, p4


def _show_geojson(img, geojson, ids, **kwargs):
    """
    Helper function to split a polygon into equidistant subplots

    Parameters:
    -----------
    img : plantcv.geospatial.images.GEO object
        geotif data, generally from read_geotif
    geojson : str
        Path to the shape file containing the regions
    ids : list
        List of plot IDs from _gather_ids

    Returns:
    --------
    plotting_img : matplotlib.pyplot
    """
    bounds = geopandas.read_file(geojson)

    # Plot the GeoTIFF
    # Make a flipped image for graphing
    flipped = img
    if len(np.shape(img.thumb)) > 2:
        flipped = cv2.merge((img.thumb[:, :, [2]],
                            img.thumb[:, :, [1]],
                            img.thumb[:, :, [0]]))

    _, ax = plt.subplots(figsize=(10, 10))
    fig_extent = plotting_extent(img[:, :, :3],
                                 img.transform)
    # Add labels to vector features
    if params.verbose and ids is not None:
        for idx, row in bounds.iterrows():
            x_coord = (row.geometry.bounds[0] + row.geometry.centroid.x) / 2
            y_coord = row.geometry.centroid.y
            plt.text(x_coord, y_coord, ids[idx], fontsize=params.text_size, c="m")

    ax.imshow(flipped, extent=fig_extent, **kwargs)
    # Plot the shapefile
    bounds.boundary.plot(ax=ax, color="blue")
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


def _gather_ids(geojson):
    """
    Helper function to gather plot IDs from a geojson if available, or auto-populate with default labels

    Parameters:
    -----------
    geojson : str
        Path to the shape file containing the regions

    Returns:
    --------
    ids : list
        List of polygon IDs
    """
    with fiona.open(geojson, 'r') as shapefile:
        # If IDs within the geojson
        ids = []
        for i, row in enumerate(shapefile):
            if 'PlotName' in row['properties']:
                ids.append((row['properties']["PlotName"]))
            elif 'ID' in row['properties']:
                ids.append((row['properties']["ID"]))
            elif 'FID' in row['properties']:
                ids.append((row['properties']["FID"]))
            elif 'plot_ids' in row['properties']:
                ids.append((row['properties']["plot_ids"]))
            else:
                # If there are no IDs in the geojson then use default labels
                ids.append(str(i + 1))
    return ids


def _plot_bounds_pseudocolored(img, geojson, vmin, vmax, data_label):
    """
    Helper function to plot shapefile bounds on a pseudocolored data layer

    Parameters:
    -----------
    img : plantcv.plantcv.classes.Spectral_data
        Spectral_data object of geotif data, used for plotting
    geojson : str
        Path to the shape file containing the regions
    vmin : float
        Minimum value to get plotted
    vmax : float
        Maximum value to get plotted
    data_label : str
        label to use when plotting

    Returns:
    --------
    analysis_image : matplotlib.pyplot
        Debug image showing shapes from geojson on input image.
    """
    # Plot the GeoTIFF
    bounds = geopandas.read_file(geojson)

    # Gather representative coordinates for each polygone in the shapefile
    bounds['coords'] = bounds['geometry'].apply(lambda x: x.representative_point().coords[:])
    bounds['coords'] = [coords[0] for coords in bounds['coords']]

    # Pseudocolor the DSM for plotting
    _, ax = plt.subplots(figsize=(10, 10))
    fig_extent = plotting_extent(img.array_data,
                                 img.metadata['transform'])
    ax.imshow(img.array_data, extent=fig_extent, cmap='viridis', vmin=vmin, vmax=vmax)

    # Plot the shapefile bounds
    bounds.boundary.plot(ax=ax, color="red")
    plt.title("Shapefile on " + str(data_label))

    # Print or plot if debug is turned on
    if params.debug is not None:
        if params.debug == 'print':
            plt.savefig(os.path.join(params.debug_outdir, str(
                params.device) + '_analyze_' + str(data_label) + '.png'), dpi=params.dpi)
            plt.close()
        elif params.debug == 'plot':
            # Use non-blocking mode in case the function is run more than once
            plt.show(block=False)
    else:
        plt.close()
    return ax


def _check_field_parameters(arglist, argnames):
    """
    Helper function check that none of the arguments are None that should be defined
    by kwargs or field_layout

    Parameters:
    -----------
    arglist : list
        list of kwargs values (after default replacement)
    argnames : list
        list of names for kwarg arguments

    Raises:
    --------
    RuntimeError if any arguments are None
    """
    if any(val is None for val in arglist):
        areNone = [val is None for val in arglist]
        noneArgs = [val for i, val in enumerate(argnames) if areNone[i]]
        fatal_error("Got None for " + str(noneArgs) + ", specify as a kwarg or add to field_layout object")
