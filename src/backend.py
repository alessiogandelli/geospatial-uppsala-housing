from flask import Flask, render_template
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from db import Database
from flask import request
import osmnx  as ox

app = Flask(__name__)

db = Database()
bus_routes = db.get_bus_routes()
bus_stops = db.get_bus_stops()
markets = db.get_supermarkets()

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
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    print(lat,lon)
    print(G)
    # G = ox.speed.add_edge_speeds(G)
    # G = ox.speed.add_edge_travel_times(G)

    #
    orig = ox.distance.nearest_nodes(G, Y=lon, X=lat)
    uni = ox.distance.nearest_nodes(G, Y=59.839815, X=17.646617)

    route = ox.shortest_path(G, orig, dest, weight="travel_time")
    edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, "length")
    print( 'length:', round(sum(edge_lengths)))

    return {'distance_uni': 77}


@app.route('/')
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(port = 8000, debug = True)