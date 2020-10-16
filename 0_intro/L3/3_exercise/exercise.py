#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise for Lecture 3:
https://github.com/AutoGIS-2017/Exercise-3

@author: cassani
"""

import csv
import geopandas as gpd
from shapely.geometry import Point


# Problem 1 Geocode shopping centers 
# Adddresses from Google for these shopping centers. Info saved as malls.txt
#
# name, id, address
# Itis, 0, "Itäkatu 1-7, 00930 Helsinki, Finland"
# Forum, 1, "Mannerheimintie 20, 00100 Helsinki, Finland"
# Iso-omena, 2, "Piispansilta 11, 02230 Espoo, Finland"
# Sello, 3, "Leppävaarankatu 3-9, 02600 Espoo, Finland"
# Jumbo, 4, "Vantaanportinkatu 3, 01510 Vantaa, Finland"
# REDI, 5, "Hermannin rantatie 5, 00580 Helsinki, Finland"

# read file as CSV 
items = []
with open('shopping_centers.txt') as fin:
  reader = csv.reader(fin, skipinitialspace=True, delimiter=',')
  headers = next(reader)
  for row in reader:
    item={}
    for ix, element in enumerate(row):
      item[headers[ix]] = element
    items.append(item)

# import as GDF
data_gdf = gpd.GeoDataFrame(items)
     
# geocodding, if error, check the timeout value (seconds)
geo_xy = gpd.tools.geocode(data_gdf['address'], provider='nominatim', user_agent='ray', timeout=5) 

# join GDF
data_gdf = data_gdf.join(geo_xy['geometry'])
# set CRS OpenStreetMap uses the WGS-84 coordinate system WGS84 == EPSG:4326
data_gdf.to_crs(epsg=4326)
# project to EPSG 3035
data_gdf = data_gdf.to_crs(epsg=3035)
# Write the data into that Shapefile
outfp = r"./shopping_centers.shp"
data_gdf.to_file(outfp)

# Problem 2 Create buffers around shopping centers
data_gdf_point = data_gdf.copy()
data_gdf['buffer'] = data_gdf['geometry'].buffer(5000)
data_gdf['geometry_point'] = data_gdf['geometry']
data_gdf['geometry'] = data_gdf['buffer']


# Problem 3 How many people live within 5 km from shopping centers?
# see: https://automating-gis-processes.github.io/2016/Lesson3-spatial-join.html#download-and-clean-the-data
# for information on Spatial Join

# Load data from population in Helsinki
pop = gpd.read_file('./Vaestotietoruudukko_2015/Vaestotietoruudukko_2015.shp')
# column ASUKKAITA (population in Finnish), inhabitants in a polygon
pop = pop.rename(columns={'ASUKKAITA': 'population'})
pop = pop[['population', 'geometry']]
# change to same CRS
pop = pop.to_crs(epsg=3035)
if not pop.crs == data_gdf.crs:
  print('Not the same CRS')

# find if one population poligon is inside a 5-km radius of the shopping centers
# This joins the GDF using the geometry columns
# keeps the geometries in 'pop', that are 'within' the geometries in data_gdf
# 'inner' says that it will keep the columns of both GDF
join = gpd.sjoin(pop, data_gdf, how="inner", op="within")
# perform summation per column 'name' of shopping center
join.groupby(['name']).sum()['population']

# Problem 4: What is the closest shopping center from your home / work?
home_add = ' Juoksuhaudantie 18 00430 Helsinki, Finland' # a random house
work_add = 'Fabianinkatu 29, 00100 Helsinki, Finland' # moomin cafe

# geocodding, if error, check the timeout value (seconds)
geo_hw = gpd.tools.geocode([home_add, work_add], provider='nominatim', user_agent='ray', timeout=5) 
# set CRS OpenStreetMap uses the WGS-84 coordinate system WGS84 == EPSG:4326
geo_hw.to_crs(epsg=4326)
# project to EPSG 3035
geo_hw = geo_hw.to_crs(epsg=3035)

def distance(point1, point2):
  return point1.distance(point2)

data_gdf_point['d_home'] = data_gdf_point['geometry'].apply(distance, args=(geo_hw.iloc[0]['geometry'],))
data_gdf_point['d_work'] = data_gdf_point['geometry'].apply(distance, args=(geo_hw.iloc[1]['geometry'],))

print('Shopping center closets to Home:')
print(data_gdf_point.iloc[data_gdf_point['d_home'].idxmin()]['name'])
print('Shopping center closets to Work:')
print(data_gdf_point.iloc[data_gdf_point['d_work'].idxmin()]['name'])
 
ax = data_gdf_point.plot(facecolor='blue')
for x, y, label in zip(data_gdf_point.geometry.x, data_gdf_point.geometry.y, data_gdf_point.name):
    ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

geo_hw.plot(ax=ax, facecolor='red')
for x, y, label in zip(geo_hw.geometry.x, geo_hw.geometry.y, ['Home', 'Work']):
    ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

