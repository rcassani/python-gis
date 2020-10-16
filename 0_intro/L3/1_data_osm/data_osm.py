#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data from OpenStreetMap using the OSMnx package
More examples of OSMnx in https://github.com/gboeing/osmnx

@author: cassani
"""

import osmnx as ox
import matplotlib.pyplot as plt

place_name = "Kamppi, Helsinki, Finland"

graph = ox.graph_from_place(place_name)

type(graph)

# DiGraph is a type that stores nodes and edges with optional data or attribs. 

# Plotting DiGraph
fig, ax = ox.plot_graph(graph, node_color='#0000FF', edge_color='#FF0000')

# getting the data a GDF
area = ox.gdf_from_place(place_name)             # area as GeoDataFrame
footprints = ox.footprints_from_place(place_name) # footprints as GeoDataFrame
nodes, edges = ox.graph_to_gdfs(graph)           # nodes and edges as GDF

# plotting data
fig, ax = plt.subplots()
area.plot(ax=ax, facecolor='#000000')
edges.plot(ax=ax, linewidth=1, edgecolor='#00FF00')
nodes.plot(ax=ax, linewidth=1, edgecolor='#0000FF')
footprints.plot(ax=ax, facecolor='#AAAAAA', alpha=0.7)
edges[edges['highway']=='footway'] .plot(ax=ax, linewidth=1, edgecolor='#FF0000')

