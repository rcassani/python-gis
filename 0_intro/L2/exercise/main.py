#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:33:19 2020
@author: cassani

Exercise 2
https://github.com/AutoGIS-2017/Exercise-2


    Problem 1: Create Polygon from lists of coordinates
    Problem 2: Points to map
    Problem 3: How long distance individuals have travelled?

"""

# Problem 1
'See file create_polygon.py'

import csv
import geopandas as gpd
from shapely.geometry import Point, LineString
from fiona.crs import from_epsg


# Problem 2: Points to map 
# read file as CSV but ; rather than ,
items = []
points = []

with open('some_posts.csv') as fin:
  reader = csv.reader(fin, skipinitialspace=True, delimiter=',')
  headers = next(reader)
  for row in reader:
    item={}
    for ix, element in enumerate(row):
      item[headers[ix]] = element
    item['coords'] = Point(float(item['lon']), float(item['lat']))
    points.append(item['coords'])
    items.append(item)

# create GeoDataFrame from dictionary
geo = gpd.GeoDataFrame(items)

# rename coords as geometry
geo = geo.rename(columns={'coords':'geometry'})

# add CRS
geo.crs = from_epsg(4326)

#plot
geo.plot()

# save shapely
outfp = r"geo_poly.shp"
geo.to_file(outfp)

# Problem 3: How long distance individuals have travelled? 
# Data is projected to EPSG:32735 projection which stands for 
# UTM Zone 35S (UTM zone for South Africa) to transform the data into 
# metric system.

# empty DataFrame
# movements = gpd.GeoDataFrame()

# list of unique users
users = geo['userid'].unique()

# project to EPSG:32735
geo_sa = geo.copy()
geo_sa = geo_sa.to_crs(epsg=32735)

# define index
geo_sa = geo_sa.set_index('userid')

# for each user
trips = []
for user in users:
  # find all points of that user
  geo_sa_user = geo_sa.loc[user]
  # if only one point do not calculate distance
  if len(geo_sa_user.shape) < 2:
    continue
  # sort by datetime
  geo_sa_user = geo_sa_user.sort_values(by='timestamp')
  # n_trips 
  n_trips = len(geo_sa_user)-1
  for ix_trip in range(n_trips):
    trip={}
    trip['userid'] = user
    trip['timestamp_ini'] = geo_sa_user.iloc[ix_trip]['timestamp']
    trip['timestamp_fin'] = geo_sa_user.iloc[ix_trip+1]['timestamp']
    trip['geometry'] = LineString([geo_sa_user.iloc[ix_trip]['geometry'], 
                                   geo_sa_user.iloc[ix_trip+1]['geometry']])
    trips.append(trip)
  
movs = gpd.GeoDataFrame(trips)
movs.crs = from_epsg(32735)
movs['distance'] = movs['geometry'].length


# What was the shortest distance travelled in meters?
movs['distance'].min()
# What was the mean distance travelled in meters?
movs['distance'].mean()
# What was the maximum distance travelled in meters?
movs['distance'].max()

# plot all trips
movs.plot()








