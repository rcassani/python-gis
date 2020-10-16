#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geocoding is converting addresses (24 Sussex Dr, Ottawa, ON K1M 1M4, Canada) 
into coordinates (45.444368, -75693835) or vice versa

@author: cassani
"""

import pandas as pd
from geopandas.tools import geocode


# Filepath
filepath = r"./addresses.txt"

# Read the data
data = pd.read_csv(filepath, sep=';')

# Geocode addresses with Nominatim backend

geo = geocode(data['addr'], provider='nominatim', user_agent='ray') 
# this geocode provider does not require API key, 
# but need a user_agent != "my-application"

# retrieved coordinates
geo.loc[0]

# joing data and geo DataFrames, based on their Index
# Only join the 'id' column
join = geo.join(data['id'])

# export the geometries to a Shaopefile
filepath_shp = r"./addresses.shp"

# Save to Shapefile
join.to_file(filepath_shp)

# Plot of the location of the addresses
join.plot()
