##################################################
#
# Mapping GPS data acquired by Arduino 
# -- using cartopy to visualize lat/lon points
# -- by parsing .csv file: gpslog.csv
#
# by Joshua Hrisko | Maker Portal LLC (c) 2021
#
##################################################
#
#
import csv
import numpy as np
import cartopy.crs as ccrs
%matplotlib
import matplotlib.pyplot as plt
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import io,time
from urllib.request import urlopen, Request
from PIL import Image
plt.ion()

def image_spoof(self, tile): # this function pretends not to be a Python script
    url = self._image_url(tile) # get the url of the street map API
    req = Request(url) # start request
    req.add_header('User-agent','Anaconda 3') # add user agent to request
    fh = urlopen(req) 
    im_data = io.BytesIO(fh.read()) # get image
    fh.close() # close url
    img = Image.open(im_data) # open image with PIL
    img = img.convert(self.desired_tile_form) # set image format
    return img, self.tileextent(tile), 'lower' # reformat for cartopy

################################
# parsing the GPS coordinates
################################
#
arduino_data = []
with open('GPSLOG.CSV','r') as dat_file:
    reader = csv.reader(dat_file)
    for row in reader:
        arduino_data.append(row)

header = arduino_data[0]
        
date,time_vec,lats,lons = [],[],[],[]
for row in arduino_data[1:]:
    date.append(row[0])
    time_vec.append(row[1])
    lats.append(float(row[2]))
    lons.append(float(row[3]))
    
#######################################
# Formatting the Cartopy plot
#######################################
#
cimgt.Stamen.get_image = image_spoof # reformat web request for street map spoofing
osm_img = cimgt.Stamen('terrain') # spoofed, downloaded street map

fig = plt.figure(figsize=(16,11)) # open matplotlib figure
ax1 = plt.axes(projection=osm_img.crs) # project using coordinate reference system (CRS) of street map
ax1.set_title('Arduino GPS Tracker Map',fontsize=16)
zoom = 0.001 # zoom out from the bounds of the data array
extent = [np.min(lons)-zoom,np.max(lons)+zoom,np.min(lats)-zoom,np.max(lats)+zoom] # map view bounds
ax1.set_extent(extent) # set extents
ax1.set_xticks(np.linspace(extent[0],extent[1],7),crs=ccrs.PlateCarree()) # set longitude indicators
ax1.set_yticks(np.linspace(extent[2],extent[3],7)[1:],crs=ccrs.PlateCarree()) # set latitude indicators
lon_formatter = LongitudeFormatter(number_format='0.1f',degree_symbol='',dateline_direction_label=True) # format lons
lat_formatter = LatitudeFormatter(number_format='0.1f',degree_symbol='') # format lats
ax1.xaxis.set_major_formatter(lon_formatter) # set lons
ax1.yaxis.set_major_formatter(lat_formatter) # set lats
ax1.xaxis.set_tick_params(labelsize=14)
ax1.yaxis.set_tick_params(labelsize=14)

scale = np.ceil(-np.sqrt(2)*np.log(np.divide((extent[1]-extent[0])/2.0,350.0))) # empirical solve for scale based on zoom
scale = (scale<20) and scale or 19 # scale cannot be larger than 19
ax1.add_image(osm_img, int(scale)) # add OSM with zoom specification

#######################################
# Plot the GPS points
#######################################
#
for ii in range(0,len(lons),10):
    ax1.plot(lons[ii],lats[ii], markersize=10,marker='o',linestyle='',
             color='#b30909',transform=ccrs.PlateCarree(),label='GPS Point') # plot points
    transform = ccrs.PlateCarree()._as_mpl_transform(ax1) # set transform for annotations

    plt.pause(0.001) # pause between point plots
