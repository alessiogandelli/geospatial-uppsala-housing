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


