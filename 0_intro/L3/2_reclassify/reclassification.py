#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reclassification

@author: cassani
"""

import zipfile
import pysal as ps
import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify as mc

# Pysal: Python library with functions and tools to do spatial data analysis

# Unzip data
with zipfile.ZipFile("data.zip","r") as zip_ref:
    zip_ref.extractall(".")

# file with square poligon, each of them is assignated with a travel time from
# it to the loacation id = 5975375 
# description of the other fields here: 
# https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015/
  
fiepath = './data/TravelTimes_to_5975375_RailwayStation.shp'
acc = gpd.read_file(fiepath)

# pt_r_tt Public transportation travel time, including time before starting the travel
# walk_d Walking distance

# The NoData values are presented with value -1
acc = acc[(acc['pt_r_tt'] >=0) & (acc['walk_d'] >=0)]

# to accelearate the plotting time, only the closest 20% of the data is kept
acc = acc.sort_values(by=['walk_d'])
n_rows = len(acc)
acc = acc.iloc[0 : n_rows // 5, : ]

# plotting PT travel times
acc.plot(column="pt_r_tt", k=9, cmap="RdYlBu", linewidth=0, scheme="Fisher_Jenks", legend=True)

# plotting by distance
acc.plot(column="walk_d", k=9, cmap="RdYlBu", linewidth=0, scheme="Fisher_Jenks", legend=True)

# classify travel times into classes
# Natural Break classification: 
# http://wiki-1-1930356585.us-east-1.elb.amazonaws.com/wiki/index.php/Jenks_Natural_Breaks_Classification
n_classes = 9
classifier = mc.NaturalBreaks.make(k=n_classes)
classifications = acc[['pt_r_tt']].apply(classifier)
classifications.columns = ['nb_pt_r_tt'] #NaturaBreak colums
acc = acc.join(classifications)
acc.plot(column="nb_pt_r_tt", linewidth=0, legend=True)

classifications = acc[['walk_d']].apply(classifier)
classifications.columns = ['nb_walk_d'] #NaturaBreak colums
acc = acc.join(classifications)
acc.plot(column="nb_walk_d", linewidth=0, legend=True)

# customized binary classification
# find the places that are less than 35 min in public transportation
# and further than 5 km.
def custom_classifier(row, col1, col2, thr1, thr2, out_col):
  if row[col1] < thr1 and row[col2] > thr2:
    row[out_col] = 1
  else:
    row[out_col] = 0
  return row

# creates column for custom_place
acc['custom_place'] = None
acc = acc.apply(custom_classifier, col1='pt_r_tt', col2='walk_d', thr1=35, thr2=5000, out_col='custom_place', axis=1)
acc.plot(column="custom_place", linewidth=0, legend=True)




