from osgeo import gdal
import matplotlib.pyplot as plt

#open geotiff and read contents into 2d array
tif_file = 'data\ASTDTM_Mosaic.tif'
dataset = gdal.Open(tif_file)

band = dataset.GetRasterBand(1) #assuming one band
elevation_data = band.ReadAsArray()#read band data into an array
print('elevation_data=',elevation_data)
transform = dataset.GetGeoTransform()

#display the geotiff image
plt.figure(figsize=(8, 6))
plt.imshow(elevation_data, extent=(transform[0], transform[0] + elevation_data.shape[1] * transform[1],
                                   transform[3] + elevation_data.shape[0] * transform[5], transform[3]), cmap='terrain')


plt.title('Geotiff Visualization')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.colorbar(label='Elevation (m)', fraction=0.046, pad=0.04)
plt.show()
