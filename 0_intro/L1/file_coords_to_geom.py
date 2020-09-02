#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problem 3: Reading coordinates from a file and creating a geometries
https://github.com/AutoGIS-2017/Exercise-1#problem-3-reading-coordinates-from-a-file-and-creating-a-geometries
"""


import csv
import numpy as np
from shapely.geometry import Point, LineString

# read file as CSV but ; rather than ,
items = []
with open('travelTimes_2015_Helsinki.txt') as fin:
  reader = csv.reader(fin, skipinitialspace=True, delimiter=';')
  headers = next(reader)
  for row in reader:
    item={}
    for ix, element in enumerate(row):
      item[headers[ix]] = element
      items.append(item)

# create lists of points      
orig_points = []
dest_points = []
lines = []
distances = []

for item in items:
   orig_point = Point(float(item['from_x']), float(item['from_y'])) 
   orig_points.append(orig_point)
   dest_point = Point(float(item['to_x']), float(item['to_y']))
   dest_points.append(dest_point)
   line = LineString([orig_point, dest_point]) 
   lines.append(line)
   distances.append(line.length)
   
distances = np.array(distances)
mean_dist = np.mean(distances)


