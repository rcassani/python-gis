#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:07:26 2020
@author: cassani



"""

import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon


###########
# Readining a shapefile with geopandas
###########
filepath = "./Europe_borders/Europe_borders.shp"
data = gpd.read_file(filepath)

# current coordinate reference system
print(data.crs)
#WGS84 == EPSG:4326: https://en.wikipedia.org/wiki/EPSG_Geodetic_Parameter_Dataset

# one example of the content of the data, it seems to be latitude-longitude
item = data.iloc[0]

# get all items with same TZID
data_berlin = data[data.TZID=='Europe/Berlin']

# Plot data with WGS84 projection
plt.figure()
plt.title("WGS84 projection")
ax = plt.gca()
data.plot(facecolor='gray', edgecolor='black', ax=ax)

# change CRS
data_proj = data.copy()
data_proj = data_proj.to_crs(epsg=3035)

plt.figure()
plt.title("EPSG3035 projection")
ax = plt.gca()
data_proj.plot(facecolor='gray', edgecolor='black', ax=ax)


