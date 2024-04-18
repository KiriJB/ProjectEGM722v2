from osgeo import gdal
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pyproj import CRS
import numpy as np
from pathlib import Path

#open geotiff and read contents into 2d array
tif_file = 'data\ASTDTM_Mosaic.tif'
csv_filename = Path(tif_file).stem #get name to give automatically created elevation profile csv file

dataset = gdal.Open(tif_file)
crs = CRS.from_string(dataset.GetProjection())
band = dataset.GetRasterBand(1) #assuming one band
elevation_data = band.ReadAsArray()#read band data into an array
transform = dataset.GetGeoTransform()#convert from row/column data to coords.

startLat, startLon = map(float, input("Enter start coordinates (x, y): ").split())
endLat, endLon = map(float, input("Enter end coordinates (x, y): ").split())
#variables to store the elevation profile start and end coordinates
#startLat = -7.122111  # longitude of point 1
#startLon = 54.843111  # latitude of point 1
#endLat = -7.125111   # longitude of point 2
#endLon = 54.691111  # latitude of point 2

#store as tuples
point1 = (startLat, startLon)
point2 = (endLat, endLon)

#Interpolate elevation data for 100 points between the 2 start and end points, number of points is a variable
#more points means a more accurate elevation profile
x1, y1 = point1 #start
x2, y2 = point2 #end

num_points = 100 #can change this variable, number of sections cross section line should be split into

#find distance between the 2 points and split into equal sections
#to find equidistant height values along the cross section line
length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

distances = np.linspace(0, np.sqrt((x2 - x1)**2 + (y2 - y1)**2), num_points)

elevation_profile = [] #array to store elevation values for profile
point_lon = []
point_lat = []
for dist in distances:
    #Calculates the x and y coordinate of the point along the line at the current distance dist.
    x = x1 + dist * (x2 - x1) / np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    y = y1 + dist * (y2 - y1) / np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    point_lon.append(x)
    point_lat.append(y)

    #get pixel location of coordinates created above
    col = int((x - transform[0]) / transform[1])
    row = int((y - transform[3]) / transform[5])

    #Retrieve the elevation from the raster dataset at the specified row and column
    #and append it to the elevation_profile list
    elevation_profile.append(elevation_data[row, col]) #append height value from pixel

df = pd.DataFrame({'Latitude': point_lat, 'Longitude': point_lon})
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

gdf.crs = {'init': 'epsg:4326'}
#need to convert distances from decimal degrees to metres (WGS84 uses metres) to display meaningful
#scale on the x axis
gdf_pcs = gdf.to_crs(epsg=3857)

#store distance for each point along the transection into an array
gdf_pcs_copy = gdf_pcs.copy()
gdf_pcs_copy['h_distance'] = 0
gdf_pcs_copy['Elevation'] = 0

# Extracting the elevations from the DEM
for index, row in gdf_pcs.iterrows():
    #print('gdf_pcs.geometry[index]=', gdf_pcs.geometry[index])
    #print('gdf_pcs.geometry[0].distance(gdf_pcs.geometry[index])=', gdf_pcs.geometry[0].distance(gdf_pcs.geometry[index]))
    temp = gdf_pcs_copy.geometry.iloc[0].distance(gdf_pcs.geometry.iloc[index])
    gdf_pcs_copy.loc[index, 'h_distance'] = int(temp)
    gdf_pcs_copy.loc[index, 'Elevation'] = elevation_profile[index]

#use min and max elevation heights from the array for the y axis
minHeight = min(elevation_profile)
maxHeight = max(elevation_profile)

# Extract h_distance (x) and Elevation (y) columns into a Pandas DataFrame
x_y_data = gdf_pcs_copy[['h_distance', 'Elevation']]
x_y_data.to_csv(r'data\ProjectCSV' + '\\' + csv_filename + '.csv')

#display the geotiff image
plt.figure(figsize=(8, 6))
minx = transform[0]
maxx = transform[0] + elevation_data.shape[1] * transform[1]
miny = transform[3] + elevation_data.shape[0] * transform[5]
maxy = transform[3]

#display the GeoTiff with a color bar
plt.imshow(elevation_data, extent=(minx, maxx, miny, maxy), cmap='terrain', aspect='auto')

# Define the start and end points for the line
line_points = [(startLat, startLon), (endLat, endLon)]
# Draw the line
x_coords, y_coords = zip(*line_points)

plt.plot(x_coords, y_coords, color='red')
plt.title('Geotiff Visualization')
plt.xlabel('Longitude', fontweight='bold')
plt.ylabel('Latitude', fontweight='bold')
plt.colorbar(label='Elevation (m)', shrink=0.7)

#display the elevation profile
plt.figure(figsize=(12, 4))
plt.plot(gdf_pcs_copy['h_distance'], gdf_pcs_copy['Elevation'], color='mediumvioletred')
plt.ylim(minHeight-10, maxHeight+10)
plt.title('Elevation Profile')
plt.xlabel('Distance (m)')
plt.ylabel('Elevation (m)')
plt.grid(True)

plt.show()
