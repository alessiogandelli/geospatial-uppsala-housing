# Geospatial analaysis of the city of Uppsala, Sweden

## Data used
- [amministrative borders](https://opendata.uppsala.se/search?groupIds=ec9ce82cb9324d22ab16db2efd2a492d): NYKO_2017_-_nivå_n.geojson
- [elevation](https://www.lantmateriet.se/sv/geodata/vara-produkter/produktlista/markhojdmodell-nedladdning-grid-50/): elevation.xyz

- [osm](https://extract.bbbike.org/?sw_lng=17.412&sw_lat=59.768&ne_lng=17.944&ne_lat=59.957&format=osm.xz&city=Uppsala&lang=en): Uppsala.osm


## Steps to reproduce

### database setup

The Uppsala.osm file have been loaded into a postgresql db using  [osm2pgsql](https://osm2pgsql.org/doc/manual.html) to do that:

- install postgres.app
- install pg4 admin 
- install osm2pgsql
- create a database in pg4admin
- create extension postgis and hstore in the database
- import the osm file to the database
  
``` osm2pgsql data/uppsala.osm -d geospatial```

### Libraries used 

geopandas, shapely, geocoder, osmnx, networkx, folium, mapclassify, pysal


## Analysis 
All the analysis can be found inside the notebook [analysis.ipynb]([uppsala.ipynb](https://github.com/alessiogandelli/geospatial-uppsala-housing/blob/main/src/analysis.ipynb))
