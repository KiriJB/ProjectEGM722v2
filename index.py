import pandas as pd
from osgeo import gdal
import geopandas as gpd
import rasterio as rio
import rasterio.merge
import shapely as shp
import earthaccess
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.widgets import Cursor
import os

'''upload a polygon shapefile to obtain boundary coordinates to search the earth access database with
to download DEM data for the area within those bounds'''


def get_dem_data():
    try:

        #boundary = gpd.read_file('Data\world-administrative-boundaries.shp') # liechtenstein
        #boundary = gpd.read_file('Data\\Andorra_Country_Boundary.shp') # Andorra
        #boundary = gpd.read_file('Data\\Counties.shp') # Northern Ireland
        boundary = gpd.read_file('Data\\Djibouti_Country_Boundary.shp') # Djibouti

        boundary = boundary.to_crs(epsg=4326)

        # gets a single polygon (or multipolygon) composed of the individual polygons
        outline = boundary['geometry'].unary_union
        # gets the minimum rotated rectangle that covers the outline
        search_area = outline.minimum_rotated_rectangle
        search_area = shp.geometry.polygon.orient(search_area, sign=1)  # a sign of 1 means oriented counter-clockwise

        earthaccess.login(strategy='netrc')
        # search for datasets that match the keyword 'elevation'
        # search for datasets that intersect Northern Ireland
        datasets = earthaccess.search_datasets(keyword='aster elevation',
                                               polygon=search_area.exterior.coords)

        dataset = datasets[0]  # get the first result
        dataset.get_umm('EntryTitle')  # fill this in with the metadata field that you want

        ds_name = dataset.get_umm(
            'ShortName')  # fill in the following with the correct field name to return the short name of the dataset

        # search for ASTER GDEM v3 granules
        # search for images that intersect our search_area
        # only show the first 10 results
        results = earthaccess.search_data(short_name=ds_name,
                                          polygon=search_area.exterior.coords, count=10)

        length = len(results)
        granule = next(iter(results))  # get the "first" item from the list



        # Create new folder to store DEM csv, png and TIF files
        f_name = input("Enter name for folder, csv, png and tif files:")
        f_name = str(f_name)
        os.makedirs(f_name, exist_ok=True)
        # download each of the granules to the aster_gdem directory
        downloaded_files = earthaccess.download(results, f_name)

        dem_files = [fn for fn in downloaded_files if 'dem.tif' in fn]  # use list
        print('dem_files=', dem_files)
        # comprehension to select only filenames that match '*dem.tif'
        if len(dem_files) > 1:
            # save mosaiced tif
            rio.merge.merge(dem_files, dst_path=f_name + '//ASTDTM_Mosaic.tif')
        else:
            if not Path(f_name + '//ASTDTM_Mosaic.tif').is_file():
                os.rename(str(dem_files[0]), f_name + '//ASTDTM_Mosaic.tif')

        return f_name

    except Exception as e:
        print("An error occurred in the get_dem_data function:", e)


# Read elevation data from a GeoTIFF file.
def get_elevation_data(tif_file1):
    try:
        print('tif_file1=', tif_file1)
        dataset = gdal.Open(tif_file1)
        #dataset = gdal.Open("LIE_Data\ASTDTM_Mosaic.tif")

        band = dataset.GetRasterBand(1)  # assuming one band
        elevation_data_temp = band.ReadAsArray()  # read band data into an array
        transform_temp = dataset.GetGeoTransform()  # convert from row/column data to co-ords.
        return elevation_data_temp, transform_temp
    except Exception as e:
        print("An error occurred in the get_elevation_data function:", e)


def onclick(event, elevation_data2, transform2):
    global click_count, start_point, end_point

    try:
        end_point = 0

        if click_count == 0:
            start_point = (event.xdata, event.ydata)
            click_count += 1
            print("First point clicked:", start_point)
        elif click_count == 1:
            end_point = (event.xdata, event.ydata)
            click_count += 1
            print("Second point clicked:", end_point)
            # Draw line between two points
            plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='red')
            plt.draw()

            # 3 Store elevation values into an array
            distances_t, elevation_profile_t, point_lat_t, point_lon_t = interpolate_elevation(elevation_data2,
                                                                                               transform2, start_point,
                                                                                               end_point)

            # 4 Convert decimal degree distances to metres from start point
            gdf_pcs_copy, min_height, max_height = convert_distance_to_metres(point_lat_t, point_lon_t,
                                                                              elevation_profile_t)

            # 5 Display elevation profile
            display_elevation_profile(gdf_pcs_copy, start_point, end_point, min_height, max_height)

            # 6 Create CSV with Height and Distance values for the elevation profile
            create_csv(gdf_pcs_copy)

    except Exception as e:
        print("An error occurred in the onclick function:", e)


# Display the GeoTiff file
def display_tiff(transform1, elevation_data1):
    try:
        # display the geotiff image
        plt.figure(figsize=(8, 6))
        minx = transform1[0]
        maxx = transform1[0] + elevation_data1.shape[1] * transform1[1]
        miny = transform1[3] + elevation_data1.shape[0] * transform1[5]
        maxy = transform1[3]

        # display the GeoTiff with a color bar
        plt.imshow(elevation_data1, extent=(minx, maxx, miny, maxy), cmap='terrain', aspect='auto')

        # display the GeoTiff with a color bar
        plt.title('Geotiff Visualization', fontweight='bold')
        plt.xlabel('Longitude', fontweight='bold')
        plt.ylabel('Latitude', fontweight='bold')
        plt.colorbar(label='Elevation (m)', shrink=0.7)
        cid = plt.gcf().canvas.mpl_connect('button_press_event',
                                           lambda event: onclick(event, elevation_data1, transform1))

        cursor = Cursor(plt.gca(), useblit=True, color='red', linewidth=1)
        print("Click 2 points on the map to draw a line for the elevation profile.")
        plt.show()

    except Exception as e:
        print('An error occurred in the display_tiff function.', e)



def check_integer():
    while True:
        num_points = input("Enter the number of points to use in elevation profile. \n"
                           "The higher the number the more detailed the profile:")
        try:
            val = int(num_points)
            if val < 0:  # if not a positive int print message and ask for input again
                print("Sorry, input must be a positive integer, try again")
                continue
            break

        except ValueError:
            print("That's not an int!")

    return val

'''Interpolate elevation data for x points between the 2 start and end points, number of points is a variable,
    more points means a more accurate elevation profile'''


def interpolate_elevation(elevation_data1, transform1, point1, point2):
    try:
        x1, y1 = point1  # start
        x2, y2 = point2  # end


        num_points = check_integer()
        #print('num points=', num_points)

        # find distance between the 2 points and split into equal sections
        # to find equidistant height values along the cross-section line
        distances = np.linspace(0, np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), num_points)

        elevation_profile = []  # array to store elevation values for profile
        point_lon = []
        point_lat = []
        for dist in distances:
            # Calculates the x and y coordinate of the point along the line at the current distance dist.
            x = x1 + dist * (x2 - x1) / np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            y = y1 + dist * (y2 - y1) / np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            point_lon.append(x)
            point_lat.append(y)

            # get pixel location of coordinates created above
            col = int((x - transform1[0]) / transform1[1])
            row = int((y - transform1[3]) / transform1[5])

            # Retrieve the elevation from the raster dataset at the specified row and column
            # and append it to the elevation_profile list
            elevation_profile.append(elevation_data1[row, col])  # append height value from pixel

        return distances, elevation_profile, point_lat, point_lon
    except Exception as e:
        print('An error occurred in the interpolate_elevation function.', e)


def convert_distance_to_metres(point_lat1, point_lon1, elevation_profile2):
    try:
        df = pd.DataFrame({'Latitude': point_lat1, 'Longitude': point_lon1})
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

        gdf.crs = ('epsg:4326')
        # need to convert distances from decimal degrees to metres (WGS84 uses metres) to display meaningful
        # scale on the x-axis
        gdf_pcs = gdf.to_crs(epsg=3857)

        '''store distance for each point from the start point to end point into an array
        store elevation data from each point into an array, to be used for x and y axis of elevation profile'''
        gdf_pcs_copy = gdf_pcs.copy()
        gdf_pcs_copy['h_distance'] = 0  # x axis
        gdf_pcs_copy['Elevation'] = 0  # y axis

        # Extracting the elevations from the DEM
        for index, row in gdf_pcs.iterrows():
            temp = gdf_pcs_copy.geometry.iloc[0].distance(gdf_pcs.geometry.iloc[index])
            gdf_pcs_copy.loc[index, 'h_distance'] = int(temp)
            gdf_pcs_copy.loc[index, 'Elevation'] = elevation_profile2[index]

        # use min and max elevation heights from the array for the y-axis
        min_height = min(elevation_profile2)
        max_height = max(elevation_profile2)
        return gdf_pcs_copy, min_height, max_height

    except Exception as e:
        print('An error occurred in the convert_distance_to_metres function.', e)


# function to create a csv file containing distance from start point and height
def create_csv(gdf_pcs_copy1):
    try:
        # Extract h_distance (x) and Elevation (y) columns into a Pandas DataFrame
        x_y_data = gdf_pcs_copy1[['h_distance', 'Elevation']]
        x_y_data.to_csv(r'' + f_name + '\\' + f_name + '.csv')
    except Exception as e:
        print("An error occurred in the create_csv function.", e)


def display_elevation_profile(gdf_pcs_copy, point1, point2, min_height, max_height):
    try:
        # display the elevation profile
        plt.figure(figsize=(12, 4))
        plt.plot(gdf_pcs_copy['h_distance'], gdf_pcs_copy['Elevation'], color='mediumvioletred')
        plt.ylim(min_height - 20, max_height + 20)
        plt.title('Elevation Profile \n' + str(round(point1[0], 6)) + ', ' + str(round(point1[1], 6)) +
                  ' to ' + str(round(point2[0], 6)) + ', ' + str(round(point2[1], 6)), fontweight='bold')
        plt.xlabel('Distance (m)', fontweight='bold')
        plt.ylabel('Elevation (m)', fontweight='bold')
        plt.grid(True)
        plt.savefig(f_name + '\\' + f_name + 'plot.png')
        plt.show()
    except Exception as e:
        print('An error occurred in the display_elevation_profile function.', e)


# Enable GDAL exceptions handling
gdal.UseExceptions()

f_name = get_dem_data()

# 1 Open geotiff and read contents into 2d array
tif_file = f_name + '\\ASTDTM_Mosaic.tif'
elevation_data, transform = get_elevation_data(tif_file)

# 2 Display GeoTiff
click_count, start_point, end_point = 0, [0, 0], [0, 0]

display_tiff(transform, elevation_data)
