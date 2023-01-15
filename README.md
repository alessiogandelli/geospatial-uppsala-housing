# geospatial-uppsala-housing
This is a project to learn how to use geospatial data and how to use it to solve a problem, in this case i want to find the best place to live in Uppsala. 

Input = an address address 
Output = distance in space and time from selected amenities ( university, supermarket, bus stop)

## run the project 
```pip install -r requirements.txt```

```python3 src/backend.py```

open a broswer and go to http://localhost:8000/





### troubleshooting with macos 

If you have problems installing the libraries probably it's because of the C packages missing, you need to install them with brew

```brew install geos ```
```brew install proj```
```brew reinstall python ```

if you get an error saying that it can't find ``` Python.h ```export these env variabless, maybe you have to change the version type, be sure that the file exists 

```export CPLUS_INCLUDE_PATH=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Headers```
```export C_INCLUDE_PATH=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Headers```


# potential data sources 
[sweden borders geopackage ](https://www.scb.se/en/services/open-data-api/open-geodata/localities/)

[other data](https://www.geodata.se/geodataportalen/srv/swe/catalog.search#/metadata/a1bff81d-5b69-483d-bd10-497ddb934b53)

[uppsala osm](https://export.hotosm.org/en/v3/exports/5c3878b4-273b-4c52-a9d5-0f17c3fdbef3) exported on demand from hotosm.org

[osm all city](https://extract.bbbike.org/)


# Tools
this is a simple web app made using python with flask and javascript with leaflet, the data is stored in a postgres database with postgis extension, the data is imported from osm files using osm2pgsql.

For the purpose of the project i'll explain better the geospatial part of the project, all the code related to this topic could be found on [geospatial_utils.py](link al file)

There is also a relevant part of the work that consisted in getting the right data from different source, but for performance porpuses in this project I first got the data and then saved to a local file.

## Data used 

- all osm data for the city of uppsala downloaded using bbbike, then the data has been saved in a postgres database using osm2pgsql, note that the data from bbike is on the https://epsg.io/900913 projection and in the database i have to convert it to the 4326 projection 


- graph of the city of uppsala saved as a graphml file after getting it using osmnx library 

```G = ox.graph_from_point( center_point=(59.8586, 17.6389), dist=8000, network_type='walk')```


## geospatial analysis

Libraries used: geopandas, osmnx, networkx, shapely, leaflet, geocoder 

### Load Bus stops ans lines
the data is saved in the db and after querying it i need to to do some transformations.

- set crs to 4326 
- filter all the bus stops relevant to me, so 4 and 12 
- for each bus stop compute the distance between the two lines and save it in a new column
- filter all the bus stops under a certain treshold 



### get closest point 

given a point and a geodataframe with points, return the closest point in the geodataframe, this is used to get the closest supermarket to home for example but can be used for any other list of equivalent points

To achieve this i have to project to the epsg 3152 (swedish grid) and then calculate the distance between the points. But then the point i return is in the ws84 projection because in the map i am using latitude and longitude as reference.

Since the Point object of the shapely library is not aware of the projection, the workaround i used was to create a geodataframe with point and projection and then use the to_crs method to convert the point to the right projection




### street network 

first task was to load the graph using osmnx library, then i had to add edge speeds and travel time in order to be able to calculate the distance between two points using the street network.

from this graph i can compute the distance between two points using the networkx library

i first get the nearest node to the point i want to start from and the point i want to reach, then i use the shortest path function to get the shortest path between the two nodes


``` start_node = ox.distance.nearest_nodes(G, Y=start.y, X=start.x) ```

then using networkx i can get the shortest path between the two nodes

```route = nx.shortest_path(G, source=source, target=target, weight='travel_time')```

then from the route i can sum all the edges traversed summing the attribute lenght to get the total lenght of the route




```nx.shortest_path_length(G, source=source, target=target, weight='travel_time')```









# 4 jan 

i played with folium and i learned how to dynamically change the tiles selecting it from the html


## query overpass api with python 
after several trials the i finally used overpass api using python to get all the bus stops and lines of uppsala using the overpass library  

```
query = '''
(
  node["highway"="bus_stop"](59.781,17.561,59.901,17.717);
  way["highway"="bus_route"](59.781,17.561,59.901,17.717);
  relation["route"="bus"](59.781,17.561,59.901,17.717);
);
'''

api = overpass.API()
response = api.get(query)

```
then i saved the output file to a osm file

## extract osm data from a big area 
is better to use https://extract.bbbike.org/ insted of overpass so you can get all the osm information for a specific area 


## osm2pgsql
the task now is to import the osm file to a postgres database, i used [osm2pgsql](https://osm2pgsql.org/doc/manual.html) to do that

- install postgres.app
- install pg4 admin 
- install osm2pgsql
- create a database in pg4admin
- create extension postgis and hstore in the database

- import the osm file to the database
```
osm2pgsql data/uppsala.osm -d geospatial

```

https://epsg.io/900913 the right projection for the osm data i imported in postgresql

bus routes and stops on the folium map from postgres 

## network 
- saved to a graphml file for working later without needing to request it again and again, graphml is the best according to [here](https://github.com/gboeing/osmnx-examples/blob/cc2308ce7deb30fda4a24e8f8eec7906bbc631e3/notebooks/05-save-load-networks.ipynb)



