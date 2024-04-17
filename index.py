from osgeo import gdal, osr
import matplotlib.pyplot as plt
from pyproj import CRS

#open geotiff and read contents into 2d array
tif_file = 'data\ASTDTM_Mosaic.tif'
dataset = gdal.Open(tif_file)
crs = CRS.from_string(dataset.GetProjection())
print('crs=', crs)

band = dataset.GetRasterBand(1) #assuming one band
elevation_data = band.ReadAsArray()#read band data into an array
print('elevation_data=', elevation_data)
transform = dataset.GetGeoTransform()#convert from row/column data to coords.

#variables to store the elevation profile start and end coordinates
startLat = -7.122111  # longitude of point 1
startLon = 54.843111  # latitude of point 1
endLat = -7.125111   # longitude of point 2
endLon = 54.691111  # latitude of point 2
#store as tuples
point1 = (startLat, startLon)
point2 = (endLat, endLon)


#display the geotiff image
plt.figure(figsize=(8, 6))
minx = transform[0]
maxx = transform[0] + elevation_data.shape[1] * transform[1]
miny = transform[3] + elevation_data.shape[0] * transform[5]
maxy = transform[3]

plt.imshow(elevation_data, extent=(minx, maxx, miny, maxy), cmap='terrain', aspect='auto')
plt.title('Geotiff Visualization')
plt.xlabel('Longitude', fontweight='bold')
plt.ylabel('Latitude', fontweight='bold')
plt.colorbar(label='Elevation (m)', shrink=0.7)
plt.show()
