# geospatial-uppsala-housing
find home in Uppsala 


# troubleshooting with macos 

if you have problems installing the libraries probably it's because of the C packages missing, you need to install them with brew

```brew install geos ```
```brew install proj```
```brew reinstall python ```

if you get an error saying that it can't find ``` Python.h ```export these env variabless, maybe you have to change the version type, be sure that the file exists 

```export CPLUS_INCLUDE_PATH=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Headers```
```export C_INCLUDE_PATH=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Headers```


# data sources 
[sweden borders geopackage ](https://www.scb.se/en/services/open-data-api/open-geodata/localities/)


[other data](https://www.geodata.se/geodataportalen/srv/swe/catalog.search#/metadata/a1bff81d-5b69-483d-bd10-497ddb934b53)


[uppsala osm](https://export.hotosm.org/en/v3/exports/5c3878b4-273b-4c52-a9d5-0f17c3fdbef3) exported on demand from hotosm.org



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



