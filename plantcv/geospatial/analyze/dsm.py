# Analyze Digital Surface Model (DSM) over many regions
from plantcv.geospatial._helpers import _gather_ids
from plantcv.plantcv import outputs, params
from rasterio.plot import plotting_extent
from matplotlib import pyplot as plt
from rasterstats import zonal_stats
import plantcv.plantcv import fatal_error
import numpy as np
import geopandas
import os


def height_percentile(dsm, geojson, lower=25, upper=90, label=None):
    """A function that analyzes elevation averages over regions and outputs data.
    Inputs:
    dsm          = Spectral_Data object of geotif data, used for affine metadata
    geojson      = Path to the shape file containing the regions for analysis
    lower        = Lower percentile cut off, input as a list formatted  default lower=25
    upper        = Upper percentile cut off, input as a list formatted  default upper=90
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    :param dsm: [spectral object]
    :param geojson: str
    :param percentile: list
    :param label: str
    """
    # DSM tifs contain just one band of data, so make the array 2D
    dsm_data = dsm.array_data[:, :, 0]
    # Cast to float since zonal_stats gives overflow error on uint8 data
    dsm_data = dsm_data.astype(np.float32)

    if dsm.metadata['nodata'] is not None:
        nodata_value = dsm.metadata['nodata']
    else:
        nodata_value = -999
    # Scale of the data
    scale = dsm.metadata["crs"].linear_units

    # Vectorize the calculation of mean elevation per region
    lower = "percentile_" + str(lower)
    region_lower_avgs = zonal_stats(geojson, dsm_data,
                                    affine=dsm.metadata["transform"],
                                    nodata=nodata_value, stats=lower)
    # Vectorize the calculation of mean elevation per region
    upper = "percentile_" + str(upper)
    region_upper_avgs = zonal_stats(geojson, dsm_data,
                                    affine=dsm.metadata["transform"],
                                    nodata=nodata_value, stats=upper)
    # Gather plot IDs from the geojson
    ids = _gather_ids(geojson=geojson)

    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    soil_vals = []
    plant_vals = []
    # Save data to outputs
    for i, id_lbl in enumerate(ids):
        # Initialize no data cases
        avg1, avg2, avg = [0.0, 0.0, nodata_value]
        # Save soil heights
        if region_lower_avgs[i][lower] is not None:
            avg1 = region_lower_avgs[i][lower]
        outputs.add_observation(sample=id_lbl, variable="soil_elevation",
                                trait="dsm_mean_below_" + str(lower),
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg1, label=label)
        soil_vals.append(avg1)
        # Save plant heights
        if region_upper_avgs[i][upper] is not None:
            avg2 = region_upper_avgs[i][upper]
        outputs.add_observation(sample=id_lbl, variable="plant_elevation",
                                trait="dsm_mean_above_" + str(upper),
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg2, label=label)
        plant_vals.append(avg2)
        if avg1 != 0 and avg2 != 0:
            avg = avg2 - avg1
        outputs.add_observation(sample=id_lbl, variable="plant_height",
                                trait="height",
                                method="plantcv-geospatial.analyze.dsm",
                                scale=scale, datatype=float,
                                value=avg, label=label)

    # Min and max height of plots
    min_elevation = min(soil_vals)
    max_elevation = max(plant_vals)

    # Plot the GeoTIFF
    bounds = geopandas.read_file(geojson)

    # Gather representative coordinates for each polygone in the shapefile
    bounds['coords'] = bounds['geometry'].apply(lambda x: x.representative_point().coords[:])
    bounds['coords'] = [coords[0] for coords in bounds['coords']]

    # Pseudocolor the DSM for plotting
    _, ax = plt.subplots(figsize=(10, 10))
    fig_extent = plotting_extent(dsm_data,
                                 dsm.metadata['transform'])
    ax.imshow(dsm_data, extent=fig_extent, cmap='viridis', vmin=min_elevation, vmax=max_elevation)

    # Plot the shapefile bounds
    bounds.boundary.plot(ax=ax, color="red")

    # Set plot title and labels
    plt.title("Shapefile on DSM")

    # Print or plot if debug is turned on
    if params.debug is not None:
        if params.debug == 'print':
            plt.savefig(os.path.join(params.debug_outdir, str(
                params.device) + '_analyze_height_percentile.png'), dpi=params.dpi)
            plt.close()
        elif params.debug == 'plot':
            # Use non-blocking mode in case the function is run more than once
            plt.show(block=False)
    else:
        plt.close()

    return bounds
    
def height_subtraction(dsm1, dsm0):
    """A function that subtracts the height of one DSM from the height of another and outputs data.
    Inputs:
    dsm1         = Spectral_Data object of geotif data, used for affine metadata - DSM with plant height
    dsm0         = Spectral_Data object of geotif data, used for affine metadata - DSM of bare ground

    Returns: 
    New Spectral_Data object which is dsm1 - dsm0.

    :param dsm1: [spectral object]
    :param dsm0: [spectral object]
    """
    #Check the coordinate reference system (CRS) is the same for both of the DSMs
    if dsm1.metadata["crs"] == dsm0.metadata["crs"]:
        pass
    else:
        fatal_error("The two input DSMs do not have the same coordinate reference system (CRS).")
    
    # DSM tifs contain just one band of data, so make the array 2D
    dsm1_data = dsm1.array_data[:, :, 0]
    dsm0_data = dsm0.array_data[:, :, 0]
    
    # Cast to float since zonal_stats gives overflow error on uint8 data
    dsm1_data = dsm1_data.astype(np.float32)
    dsm0_data = dsm0_data.astype(np.float32)

    if dsm1.metadata['nodata'] is not None:
        nodata_value = dsm1.metadata['nodata']
    else:
        nodata_value = -999
        
    if dsm0.metadata['nodata'] is not None:
        nodata_value = dsm0.metadata['nodata']
    else:
        nodata_value = -999
        
    # Scale of the data
    scale1 = dsm1.metadata["crs"].linear_units
    scale0 = dsm0.metadata["crs"].linear_units

    #Perform the subtraction
    final_subtraction = dsm1_data - dsm0_data

    return final_subtraction
    
