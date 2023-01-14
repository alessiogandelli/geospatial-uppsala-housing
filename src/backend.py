from flask import Flask, render_template
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from db import Database
from flask import request
import osmnx  as ox
import networkx as nx
from shapely.geometry import Point, Polygon
import geocoder


app = Flask(__name__)

db = Database()
bus_routes = db.get_bus_routes()
bus_stops = db.get_bus_stops()
markets = db.get_supermarkets()

centrum =  Point([17.6387, 59.8586])
uni = Point([ 17.646617, 59.839815])

#centrum = gpd.GeoDataFrame({'geometry': centrum}, index=[0], crs="EPSG:4326").to_crs(epsg=3152).geometry[0]
#uni = gpd.GeoDataFrame({'geometry': uni}, index=[0], crs="EPSG:4326").to_crs(epsg=3152).geometry[0]


bus_routes = bus_routes.set_index('ref')

# prjoject to meters 
# bus_stops = bus_stops.to_crs(epsg=3152)
# bus_routes = bus_routes.to_crs(epsg=3152)

#prjoject to meters 
bus_stops = bus_stops.to_crs(epsg=4326)
bus_routes = bus_routes.to_crs(epsg=4326)

# for each bus stop get distance from 4 taken from bus_routes
bus_stops['distance4'] = bus_stops.apply(lambda row: row.geometry.distance( bus_routes.loc[4]['geometry']), axis=1)
bus_stops['distance12'] = bus_stops.apply(lambda row: row.geometry.distance( bus_routes.loc[12]['geometry']), axis=1)



# get bus stop in a 20 meters radius from bus route 4 or 12 
bus_stops = bus_stops.loc[(bus_stops['distance4'] < 0.0005) | (bus_stops['distance12'] < 0.0005)]
# keep only bus routes 4 and 12
bus_routes = bus_routes.loc[[4, 12]]


G = ox.load_graphml("/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/street_network.graphml")
print('street nextword loaded', G)


@app.route('/stops')
def stops():
    return bus_stops.to_crs(epsg = 4326).to_json()

@app.route('/routes')
def routes():
    return bus_routes.to_crs(epsg = 4326).to_json()

@app.route('/supermarkets')
def supermarkets():
    return markets.to_crs(epsg = 4326).to_json()


@app.route('/score')
def score():
    global bus_stops
    response = {}
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    
    home = Point([lon, lat])
    #home = gpd.GeoDataFrame({'geometry': home}, index=[0], crs="EPSG:4326").to_crs(epsg=3152).geometry[0]


    closest_stop_idx = bus_stops.distance(home).sort_values().index[0]
    closest_stop = bus_stops.loc[closest_stop_idx]

    distance_stop = get_distance(closest_stop[1], home)

    closest_supermarket_idx = markets.distance(home).sort_values().index[0]
    closest_supermarket = markets.loc[closest_supermarket_idx]
    distance_supermarket = get_distance(closest_supermarket[1], home)


    bus_lines = get_bus_lines(closest_stop[1])

    home_uni = get_distance(home, uni)
    home_center = get_distance(home, centrum)

    print(home_uni, home_center)


    place = geocoder.osm([lat, lon], method='reverse')


    
    
    response['address'] = place.address
    response['home_lat'] = lat
    response['home_lon'] = lon

    response['bus_closest_name'] = closest_stop[0]
    response['bus_closest_lat'] = closest_stop.geometry.xy[1][0]
    response['bus_closest_lon'] = closest_stop.geometry.xy[0][0]
    response['bus_stop_distance'] = round(distance_stop)

    response['home_uni'] = round(home_uni)
    response['home_center'] = round(home_center)
    response['home_supermarket'] = round(distance_supermarket)


    return response


def get_distance(start, end):
    global G
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    #start = gpd.GeoDataFrame({'geometry': start}, index=[0], crs="EPSG:3153").to_crs(epsg=4326).geometry[0]
    #end = gpd.GeoDataFrame({'geometry': end}, index=[0], crs="EPSG:3152").to_crs(epsg=4326).geometry[0]

    start_node = ox.distance.nearest_nodes(G, Y=start.y, X=start.x)
    end_node = ox.distance.nearest_nodes(G, Y=end.y, X=end.x)

    route = nx.shortest_path(G, start_node, end_node, weight='travel_time')
    
    edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length')
    distance = sum(edge_lengths)

    return distance


def get_bus_lines(start):
    # find the closest line from this  bus stop, after a threshold
    pass

@app.route('/heatmap')
def heatmap():
    trip_times = [3, 6, 9, 15]  # in minutes
    travel_speed = 4  # walking speed in km/hour

    center_node =  ox.distance.nearest_nodes(G, Y=59.839815, X=17.646617)

    G_proj = ox.project_graph(G)

    #add an edge attribute for time in minutes required to traverse each edge
    meters_per_minute = travel_speed * 1000 / 60  # km per hour to m per minute
    for orig,dest, p, data in G_proj.edges(data=True, keys=True):
        data["time"] = data["length"] / meters_per_minute

    isochrone_polys = []
    for trip_time in sorted(trip_times, reverse=True):
        subgraph = nx.ego_graph(G_proj, center_node, radius=trip_time, distance="time")
        node_points = [Point((data["x"], data["y"])) for node, data in subgraph.nodes(data=True)]
        bounding_poly = gpd.GeoSeries(node_points).unary_union.convex_hull
        isochrone_polys.append(bounding_poly)

    # to geojson 
    data = {'trip_time': sorted(trip_times, reverse=True), 'geometry': isochrone_polys}
    crs_proj = ox.graph_to_gdfs(G_proj)[0].crs

    isochrones = gpd.GeoDataFrame(data,crs=crs_proj)

    return isochrones.to_json()




@app.route('/')
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(port = 8000, debug=True)