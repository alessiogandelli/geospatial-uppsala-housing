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

bus_routes = bus_routes.set_index('ref')


G = ox.load_graphml("/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/street_network.graphml")
print('street nextword loaded', G)


@app.route('/stops')
def stops():
    return bus_stops.to_json()

@app.route('/routes')
def routes():
    return bus_routes.to_json()

@app.route('/supermarkets')
def supermarkets():
    return markets.to_json()


@app.route('/score')
def score():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    response = {}

    home = Point([lon, lat])
    closest_idx = bus_stops.distance(home).sort_values().index[0]
    closest = bus_stops.iloc[closest_idx]

    distance = get_distance(closest[1], home)


    place = geocoder.osm([lat, lon], method='reverse')


    
    
    response['address'] = place.address
    response['bus_closest_name'] = closest[0]
    response['bus_closest_lat'] = closest.geometry.xy[1][0]
    response['bus_closest_lon'] = closest.geometry.xy[0][0]
    response['home_lat'] = lat
    response['home_lon'] = lon
    response['bus_stop_distance'] = distance




    return response


def get_distance(start, end):
    global G
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    start_node = ox.distance.nearest_nodes(G, Y=start.y, X=start.x)
    end_node = ox.distance.nearest_nodes(G, Y=end.y, X=end.x)

    route = nx.shortest_path(G, start_node, end_node, weight='travel_time')
    
    edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length')
    distance = sum(edge_lengths)

    return distance

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
    app.run(port = 8000)