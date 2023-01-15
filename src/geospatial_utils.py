

import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import geospatial_utils as geo
from flask import request
import osmnx  as ox
import networkx as nx
from shapely.geometry import Point, Polygon
import geocoder

def get_score(home, bus_stops, markets, uni, centrum, G):

    response = {}
    # get closest points from home
    closest_stop = get_closest_point(home, bus_stops)
    closest_supermarket = get_closest_point(home, markets)


    # compute distances 
    home_supermarket = get_distance(home, closest_supermarket[1], G)
    home_bus        = get_distance(home,closest_stop[1], G)
    home_uni             = get_distance(home, uni, G)
    home_center          = get_distance(home, centrum, G)


    # get home address from coords
    place = geocoder.osm([home.y, home.x], method='reverse')


    response['address'] = place.address
    response['home_lat'] = home.y
    response['home_lon'] = home.x

    response['bus_closest_name'] = closest_stop[0]
    response['bus_closest_lat'] = closest_stop.geometry.y
    response['bus_closest_lon'] = closest_stop.geometry.x

    response['home_uni'] = round(home_uni)
    response['home_center'] = round(home_center)
    response['home_supermarket'] = round(home_supermarket)
    response['home_bus'] = round(home_bus)

    return response


# get two points as input and return the distance between them
def get_distance(start, end, G):
    print('start', start, type(start))

    #find closest node in the network to the start and end points
    start_node = ox.distance.nearest_nodes(G, Y=start.y, X=start.x)
    end_node   = ox.distance.nearest_nodes(G, Y=end.y, X=end.x)

    #find the shortest path between the nodes according to the travel time 
    route = nx.shortest_path(G, start_node, end_node, weight='travel_time')
    
    #get the length of the route
    edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length')
    distance = sum(edge_lengths)

    return distance


def load_graph():
    G = ox.load_graphml("/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/street_network.graphml")
    print('street nextword loaded', G)

    # add travel time to each edge 
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    return G


def get_bus(bus_stops, bus_routes):
    print('preparing bus stops and routes')
    # set crs
    bus_stops = bus_stops.set_crs(epsg=4326)
    bus_routes = bus_routes.set_crs(epsg=4326)

    # for each bus stop get distance from 4 and 12 routes
    bus_stops['distance4'] = bus_stops.apply(lambda row: row.geometry.distance( bus_routes.loc[4]['geometry']), axis=1)
    bus_stops['distance12'] = bus_stops.apply(lambda row: row.geometry.distance( bus_routes.loc[12]['geometry']), axis=1)

    # filter stops and routes to the ones that pass from the uni
    bus_stops = bus_stops.loc[(bus_stops['distance4'] < 0.0005) | (bus_stops['distance12'] < 0.0005)]
    bus_routes = bus_routes.loc[[4, 12]]


    return bus_stops, bus_routes


def get_closest_point(point, gdf):
    print('getting closest point to ')
    point_proj = gpd.GeoDataFrame({'geometry': point}, index=[0], crs="EPSG:4326").to_crs(epsg=3152).geometry[0]

    # get the closest bus stop get the closest bus stop
    closest_idx = gdf.to_crs(epsg = 3152).distance(point_proj).sort_values().index[0]
    closest = gdf.loc[closest_idx] 

    return closest