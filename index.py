from tkinter import *
import pandas as pd
from osgeo import gdal
import geopandas as gpd
import rasterio as rio
import rasterio.merge
import shapely as shp
import earthaccess
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splrep, splev
from colorama import Fore, Back
from pathlib import Path
from matplotlib.widgets import Cursor
import math
import os


def get_dem_data():
    """
    Upload a polygon shapefile to obtain boundary coordinates these are used by the earth access
    database to find DEM data within those bounds, this data is downloaded mosaicked and saved locally as a tiff
    Create folder to store files in

    Returns:
    string: The name input by the user for folder to store new files and name files
    """
    try:
        while True:
            boundary = input(Fore.LIGHTBLUE_EX + "\n\nEnter the name of the Shapefile that you have saved to the Data "
                                                 "folder, that you wish to use \n for this analysis "
                                                 "ie.andorra_country_boundary.shp:\n" + Fore.GREEN)
            # check for user input
            if not boundary:
                print('You did not enter a filename. Try Again!')
                boundary = input(
                    Fore.LIGHTBLUE_EX + "\n\nEnter the name of the Shapefile that you have saved to the Data "
                                        "folder, that you wish to use \n for this analysis "
                                        "ie.andorra_country_boundary.shp:\n" + Fore.GREEN)

            # Example shape files you could use that are stored in the data folder
            # Liechtenstein_Country_Boundary.shp (liechtenstein), purbeck_boundary.shp
            # Andorra_Country_Boundary.shp (Andorra), Counties.shp (Northern Ireland)
            # Djibouti_Country_Boundary.shp (Djibouti)

            boundary_path = 'Data\\' + str(boundary)
            #boundary_path = ''

            if os.path.exists(boundary_path):
                boundary = gpd.read_file(boundary_path)
                print(Fore.LIGHTYELLOW_EX + "\nYay! File found, please wait while we find DEM data for this area from NASA Earthdata.")
                break
            else:
                print(Fore.LIGHTYELLOW_EX + "\nFile does not exist. Please enter a valid filename. (ie. andorra_country_boundary.shp)")

        boundary = boundary.to_crs(epsg=4326)

        # gets a single polygon (or multipolygon) composed of the individual polygons
        outline = boundary['geometry'].unary_union

        # gets the minimum rotated rectangle that covers the outline
        search_area = outline.minimum_rotated_rectangle
        search_area = shp.geometry.polygon.orient(search_area, sign=1)  # a sign of 1 means oriented counter-clockwise

        earthaccess.login(strategy='netrc')

        # search for datasets that match the keyword 'elevation' and
        # that intersect the selected shapefile polygon area
        datasets = earthaccess.search_datasets(keyword='aster elevation',
                                               polygon=search_area.exterior.coords)

        dataset = datasets[0]  # get the first result
        dataset.get_umm('EntryTitle')  # fill this in with the metadata field that you want

        # fill in the following with the correct field name to return the short name of the dataset
        ds_name = dataset.get_umm('ShortName')

        # search for ASTER GDEM v3 granules
        # search for images that intersect our search_area
        # only show the first 10 results
        results = earthaccess.search_data(short_name=ds_name,
                                          polygon=search_area.exterior.coords)

        granule = next(iter(results))  # get the "first" item from the list

        # Create new folder to store DEM csv, png and TIF files
        print(Fore.LIGHTBLUE_EX + "\nWe need to create a folder to store the DEM data in, and set file names\n"
              "for the CSV and PNG files that will be created.")
        f_name = input("Please enter a name for the folder and files (eg andorra):\n" + Fore.GREEN)

        # check for user input
        if not f_name:
            print('You did not enter a name. Try Again!')
            boundary = input(
                Fore.LIGHTBLUE_EX + "\nWe need to create a folder to store the DEM data in, and set file names\n"
              "for the CSV and PNG files that will be created." + Fore.GREEN)

        print(Fore.RED)
        f_name = str(f_name+"_Data")
        os.makedirs(f_name, exist_ok=True)

        # download each of the granules to the aster_gdem directory
        downloaded_files = earthaccess.download(results, f_name)

        dem_files = [fn for fn in downloaded_files if 'dem.tif' in fn]  # use list

        # comprehension to select only filenames that match '*dem.tif'
        if len(dem_files) > 1:
            # save mosaicked tif
            rio.merge.merge(dem_files, dst_path=f_name + '//ASTDTM_Mosaic.tif')
        else:
            if not Path(f_name + '//ASTDTM_Mosaic.tif').is_file():
                os.rename(str(dem_files[0]), f_name + '//ASTDTM_Mosaic.tif')

        print(Fore.LIGHTWHITE_EX + "\nASTDTM_Mosaic.tif created and saved to " + f_name + "/ASTDTM_Mosaic.tif\n")

        return f_name

    except Exception as e:
        print(Back.RED + 'An error occurred in the get_dem_data function:', e)


def get_elevation_data(tif_file1):
    """
    Read elevation data from a GeoTIFF file.
    Parameters:
    tif_file1(string): location of the Geotiff file created from earthaccess data and stored locally

    Returns:
    string: The name input by the user for folder to store new files and name files
    """
    try:
        dataset = gdal.Open(tif_file1)
        band = dataset.GetRasterBand(1)  # assuming one band
        elevation_data_temp = band.ReadAsArray()  # read band data into an array
        transform_temp = dataset.GetGeoTransform()  # convert from row/column data to co-ords.
        return elevation_data_temp, transform_temp

    except Exception as e:
        print(Back.RED + 'An error occurred in the get_elevation_data function:', e)


def display_tiff(transform1, elevation_data1):
    """
    Display the geotiff file created from the EarthAccess data.

    Parameters:
    transform1(dataset): lat/lon data from geotiff
    elevation_data1(list): Store elevation data in a list from geotiff
    """
    try:
        # display the geotiff image
        plt.figure(figsize=(8, 6))
        minx = transform1[0]
        maxx = transform1[0] + elevation_data1.shape[1] * transform1[1]
        miny = transform1[3] + elevation_data1.shape[0] * transform1[5]
        maxy = transform1[3]

        # display the GeoTiff with a title, axis and color bar
        plt.imshow(elevation_data1, extent=(minx, maxx, miny, maxy), cmap='terrain', aspect='auto')
        plt.title(label='Geotiff Digital Elevation Model', fontweight='bold')
        plt.xlabel(xlabel='Longitude', fontweight='bold')
        plt.ylabel(ylabel='Latitude', fontweight='bold')
        plt.colorbar(label='Elevation (m)', shrink=0.7)
        cursor = Cursor(plt.gca(), useblit=True, color='red', linewidth=1)


        print(Fore.LIGHTBLUE_EX + "Click 2 points on the map to draw a line that will be used for "
                                  "the elevation profile:")
        # Get user clicks using ginput
        click_coords = plt.ginput(2)

        # Convert pixel coordinates to geographic coordinates
        for i, (lat, lon) in enumerate(click_coords, start=1):
            if i == 1:
                start_point = [lat, lon]
                print(Fore.LIGHTYELLOW_EX + 'Start point:', start_point)
            elif i == 2:
                end_point = [lat, lon]
                print(Fore.LIGHTYELLOW_EX + 'End point:', end_point)

        # hide tkinter window
        root.withdraw()

        # Draw a line between two points on the DEM
        plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='red')
        plt.draw()

        # check if file exists, if not create a new file with a number appended to the filename
        path_dem = uniquify(f_name + '\\' + f_name + '_DEM.png')
        plt.savefig(path_dem)

        print(Fore.LIGHTWHITE_EX + "\nPNG image file of the DEM created and stored in Data\\" + path_dem + "\n")

        # Step 4 - Store elevation values into an array
        distances_t, elevation_profile_t, point_lat_t, point_lon_t = interpolate_elevation(elevation_data1,
                                                                                           transform1, start_point,
                                                                                           end_point)

        # Step 5 - Convert decimal degree distances to metres from start point
        gdf_pcs_copy, min_height, max_height, max_dist = convert_distance_to_metres(point_lat_t, point_lon_t,
                                                                                    elevation_profile_t)

        # Step 6 - Create CSV with Height and Distance values for the elevation profile
        create_csv(gdf_pcs_copy)

        # Step 7 - Display elevation profile
        display_elevation_profile(gdf_pcs_copy, start_point, end_point, min_height, max_height, max_dist)


    except Exception as e:
        print(Back.RED + 'An error occurred in the display_tiff function.', e)



def check_integer(str_input):
    """
    Check the input value is a +ive integer.

    Parameters:
    str_input(string): input string, asking for integer

    Returns:
    int: returns an integer
    """
    try:
        while True:
            num_points1 = input(str_input + Fore.GREEN)
            try:
                val = int(num_points1)
                if val < 0:  # if not a positive int print message and ask for input again
                    print(Fore.LIGHTYELLOW_EX + 'Sorry, input must be a positive integer, try again')
                    continue
                break

            except ValueError:

                print(Fore.LIGHTYELLOW_EX + 'That is not an int!')  # if letters are entered then show this message

        return val

    except EOFError:
        print(Back.RED + 'Input stream ended unexpectedly. Please try again.')
        return None  # or take appropriate action


def interpolate_elevation(elevation_data1, transform1, point1, point2):
    """
    Interpolate elevation data for x points between the start and end points, number of points is a variable,
    a higher value will mean a more accurate elevation profile.

    Parameters:
    elevation_data1(list of integers): Store elevation data in a list from geotiff
    transform1(dataset): lat/lon data from geotiff
    point1(list of floats): Start point of line to use for the elevation profile(lat/lon)
    point2(list of floats): End point of line to use for the elevation profile(lat/lon)

    Returns:
    distances, elevation_profile, point_lat, point_lon
    list: list of distances stored as latitude / longitudes
    elevation_profile : list of heights along the elevation profile line
    list: latitude for each point along the elevation profile line
    list: longitude for each point along the elevation profile line
    """
    try:
        x1, y1 = point1  # start
        x2, y2 = point2  # end

        # request the number of points to get elevation data for between
        # the selected start and end points
        print(Fore.LIGHTBLUE_EX + "The number of points entered here will be used to calculate equidistant points along"
              " the elevation profile,\n"
              "elevation data at each point will be extracted from the DEM and used to create the elevation profile.")

        str_question = "Enter the number of points to use to calculate the elevation profile. ie 200:\n"

        # validate that an integer has been entered
        num_points = check_integer(str_question)

        # find distance between the 2 points and split into equal sections
        # to find equidistant height values along the cross-section line
        distances = np.linspace(0, np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), num_points)

        elevation_profile = []  # array to store elevation values for profile
        point_lon = []
        point_lat = []

        for dist in distances:

            # Calculates the x and y coordinate of the point along the line at the current dist.
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
        print(Back.RED + 'An error occurred in the interpolate_elevation function:', e)


def convert_distance_to_metres(point_lat1, point_lon1, elevation_profile2):
    """
    Convert distance to each point from the start point from decimal degrees to metres

    Parameters:
    point_lat1(list of integers): Start point of elevation profile line
    point_lon1(list of integers): End point of elevation profile line
    elevation_profile2(list of integers): Store elevation data in a list from geotiff

    Returns:
    gdf_pcs_copy, min_height, max_height, max_distance
    dataframe : containing distance of each point in metres from the start point and elevation values for each point
    int : minimum height value in the geodataset for the y-axis
    int : maximum height value in the geodataset for the y-axis
    int : distance in metres from the start to end points for the elevation profile
    """
    try:
        df = pd.DataFrame({'Latitude': point_lat1, 'Longitude': point_lon1})
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

        gdf.crs = 'epsg:4326'
        # need to convert distances from decimal degrees to metres (WGS84 uses metres) to display meaningful
        # scale on the x-axis
        gdf_pcs = gdf.to_crs(epsg=3857)

        # store distance for each point from the start point to end point into an array store
        # elevation data from each point into an array, to be used for x and y-axis of elevation profile
        gdf_pcs_copy = gdf_pcs.copy()
        gdf_pcs_copy['h_distance'] = 0  # x axis
        gdf_pcs_copy['Elevation'] = 0  # y axis

        distance_array = []

        # Extracting the elevations from the DEM
        for index, row in gdf_pcs.iterrows():
            temp = gdf_pcs_copy.geometry.iloc[0].distance(gdf_pcs.geometry.iloc[index])
            distance_array.append(int(temp))
            gdf_pcs_copy.loc[index, 'h_distance'] = int(temp)
            gdf_pcs_copy.loc[index, 'Elevation'] = elevation_profile2[index]

        # use min and max elevation heights from the array for the y-axis
        min_height = min(elevation_profile2)
        max_height = max(elevation_profile2)

        # get the furthest distance
        max_distance = max(distance_array)
        print('')

        return gdf_pcs_copy, min_height, max_height, max_distance

    except Exception as e:
        print(Back.RED + 'An error occurred in the convert_distance_to_metres function.', e)


def create_csv(gdf_pcs_copy1):
    """
    Function to create a csv file containing distance and height of each point from start of elevation profile

    Parameters:
    gdf_pcs_copy1(dataframe): containing distance of each point in metres from the start
    point and elevation values for each point.
    """
    try:
        # Extract h_distance (x) and Elevation (y) columns into a Pandas DataFrame
        x_y_data = gdf_pcs_copy1[['h_distance', 'Elevation']]

        # check if file exists, if it does, create a new file with a number appended to the filename
        path_csv = uniquify(f_name + '\\' + f_name + '_data.csv')
        x_y_data.to_csv(r'' + path_csv)
        print(Fore.LIGHTWHITE_EX + "CSV file of elevation data for profile created and stored in \\" + path_csv)

    except Exception as e:
        print(Back.RED + 'An error occurred in the create_csv function.', e)


def uniquify(path):
    """
    Function to create a new file if one already exists with the specified name with a number that increments
    source - https: // stackoverflow.com / questions / 13852700 / create - file - but - if -name - exists - add - number

    Parameters:
    path(string): path of file, to check if it exists

    Returns:
    string : path of the new file and its filename
    """

    filename, extension = os.path.splitext(path)
    counter = 1

    # append a number to the filename if file already exists
    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


def display_elevation_profile(gdf_pcs_copy, point1, point2, min_height, max_height, max_dist):
    """
    Display the elevation profile. User inputs how many metres to split the elevation profile into.

    Parameters:
    gdf_pcs_copy(dataframe) : containing distance of each point in metres from the start
    point1(list of floats) : lat/lon of start point
    point2(list of floats) : lat/lon of end point
    min_height(int) : minimum height value in the geodataset for the y-axis
    max_height(int) : maximum height value in the geodataset for the y-axis
    max_dist(int) : distance of the elevation profile
    """
    global t_list, new_count

    try:
        print(Fore.LIGHTYELLOW_EX + "\nSelected elevation profile distance in metres " + str(max_dist) + "(m)\n")

        str_question = (Fore.LIGHTBLUE_EX + "Split the elevation profile into subplots in metres \n"
                                            "ie if the profile distance is "
                        "9,600m you could enter 2500 to split the profile into 4 x 2,500m subplots,\n"
                        "enter 1 to not split the profile over numerous subplots:\n ")

        # divide the distance by n to calculate the number of plots
        xsection_dist = check_integer(str_question)

        # if value entered is > than max distance or value entered = 1 then display 1 subplot
        if (max_dist < xsection_dist) or (xsection_dist == 1):
            number_of_plots = 1
        elif max_dist >= xsection_dist:
            number_of_plots = math.floor(max_dist / xsection_dist) + 1

        # set the figure size
        fig, ax = plt.subplots(number_of_plots, ncols=1,
                               figsize=(12, 4 * number_of_plots) if number_of_plots > 1 else (12, 4))

        # set the subplot title
        fig.suptitle('Elevation Profile \n' + str(round(point1[0], 6)) + ', ' + str(round(point1[1], 6)) +
                     ' to ' + str(round(point2[0], 6)) + ', ' + str(round(point2[1], 6)) + ', ' +
                     str(max_dist) + 'm \n', fontweight='bold')

        n = 0
        # if 1 entered then set xsection_dist to entire profile length
        if xsection_dist == 1:
            xsection_dist = max_dist

        add_count = xsection_dist  # split x-axis into subplots of n(m)

        # create individual subplot elevation profiles for each n(m) section
        for ax_i in ax if isinstance(ax, np.ndarray) else [ax]:
            if n == 0:
                t_list = gdf_pcs_copy[gdf_pcs_copy['h_distance'] < add_count]
                new_count = add_count
            else:
                t_list = gdf_pcs_copy[(gdf_pcs_copy['h_distance'] > (new_count + 1)) &
                                      (gdf_pcs_copy['h_distance'] < (new_count + add_count))]
                new_count = new_count + add_count

            # create a list of the elevation column data in the geodataframe
            sub_list = gpd.GeoDataFrame(t_list)
            x_values = sub_list['h_distance']  # x-values are the distances along the route
            y_values = sub_list['Elevation']  # y-values are the elevations at each distance
            baseline = 0

            # Interpolate elevation values using spline interpolation
            tck = splrep(x_values, y_values)
            x_new = np.linspace(min(x_values), max(x_values), 1000)
            y_smooth = splev(x_new, tck)

            # Calculate lower and upper y-values for filling
            y_lower_values = np.minimum(y_smooth, baseline)
            y_upper_values = np.maximum(y_smooth, baseline)

            # Plot the smoothed curve
            ax_i.plot(x_new, y_smooth, color='seagreen')

            ax_i.set_ylim(min_height - 20, max_height + 20)
            x = [new_count - add_count, new_count]
            ax_i.set_xlim(new_count - add_count, new_count)
            ax_i.set_xlabel('Distance (m)', fontweight='bold')
            ax_i.set_ylabel('Elevation (m)', fontweight='bold')
            # Fill between the curve and the baseline
            ax_i.fill_between(x_new, y_lower_values, y_upper_values, color='palegreen', alpha=0.5)
            ax_i.grid(True)
            n += 1

        fig.tight_layout()

        # check if file exists, if not create a new file with a number appended to the filename
        path_plot = uniquify(f_name + '\\' + f_name + '_profile.png')
        plt.savefig(path_plot)

        # check if file exists, if not create a new file with a number appended to the filename
        path_plt_pdf = uniquify(f_name + '\\' + f_name + '_profile.pdf')
        plt.savefig(path_plt_pdf, bbox_inches='tight')

        os.startfile(path_plt_pdf)  # open the pdf file

        print(Fore.LIGHTWHITE_EX + "\nPNG image file of the elevation profile created and stored in " + path_plot)
        print(Fore.LIGHTWHITE_EX + "PDF of the elevation profile created and stored in " + path_plt_pdf)

        print(Fore.MAGENTA + "\nTHE END!")

        plt.draw()
        # quit()

    except Exception as e:
        print(Back.RED + 'An error occurred in the display_elevation_profile function.', e)


global cursor, cid

# Enable GDAL exceptions handling
gdal.UseExceptions()

# Step 1 - Call function to get the DEM data from NASA Earthaccess
f_name = get_dem_data()

# Step 2 - Open geotiff and read contents into 2d array
tif_file = f_name + '\\ASTDTM_Mosaic.tif'
elevation_data, transform = get_elevation_data(tif_file)

# declare variables
click_count, start_point, end_point = 0, [0, 0], [0, 0]

# Step 3 - Display GeoTiff using Tkinter to start a separate event loop and call display_tiff function
root = Tk()
root.title("View the GeoTIFF")
root.geometry("300x100")
colorfg = '#3F4F4C'
colorbg = '#C0D6E4'
my_button = Button(root, text="Click to View GeoTIFF", relief='flat', justify='center', font="sans 12 bold", bg=colorbg,
                   fg=colorfg, command=lambda: display_tiff(transform, elevation_data))
my_button.place(relx=0.5, rely=0.5, anchor=CENTER)
my_button.pack(padx=0, pady=30)

# Make the window jump above all
root.attributes('-topmost', True)
root.mainloop()
