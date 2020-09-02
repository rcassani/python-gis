#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 09:58:54 2020
@author: cassani

Data is the world distribution of the Damselfish, divided per species 
a total of 30 species.
The values for the Polygons are given in degrees (coordinates)
+x East
-x West
+y North
-y South
With geopandas, the shapes of the shapeline file are stored in the 'geometry'
field in the dataframe
"""


import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon

###########
# Readining a shapefile with geopandas
###########

filepath = 'Data/DAMSELFISH_distributions.shp'
data = gpd.read_file(filepath)

# get list of damselfish species
species = data.BINOMIAL.unique()

for specie in species[0:1]:
  data_species = data[data.BINOMIAL == specie]
  # geopandas is used to compute directly the area for each geometry
  data_species['area'] = data_species.area
  # plot all the geometries
  data_species.plot()
  fig = plt.gca()
  fig.set_title(specie)
  print(len(data_species))
  
###########
# Writing shapes to a shapefiles with geopandas
###########

# Create an empty geopandas GeoDataFrame
newdata = gpd.GeoDataFrame()
newdata['geometry'] = None

# Coordinates of the Helsinki Senate square in Decimal Degrees
coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]

# Create a Shapely polygon from the coordinate-tuple list
poly = Polygon(coordinates)
  
newdata.loc[0, 'geometry'] = poly
newdata.loc[0, 'Location'] = 'Helsinki Senate'

newdata.plot()

#Determine the coordinate reference system (projection) CRS for GeoDataFrame
print(newdata.crs)  

# Import specific function 'from_epsg' from fiona module
# European Petroleum Survey Group, EPSG registry is a public registry of spatial reference systems
from fiona.crs import from_epsg

# Set the GeoDataFrame's coordinate system to WGS84
#WGS84 == EPSG:4326: https://en.wikipedia.org/wiki/EPSG_Geodetic_Parameter_Dataset
newdata.crs = from_epsg(4326)

# Let's see how the crs definition looks like
newdata.crs

outfp = r"helsinki_senate.shp"

# Write the data into that Shapefile
newdata.to_file(outfp)
