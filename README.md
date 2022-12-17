# geospatial-uppsala-housing
find home in Uppsala 


# troubleshooting with macos 

if you have problems installing the libraries probably it's because of the C packages you need to install them with brew

```brew install geos ```
```brew install proj```
```brew reinstall python ```

if you get an error saying that it can found  Python.h export this env variables, maybe you have to change the version type, be sure that this file exists 

```export CPLUS_INCLUDE_PATH=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Headers```
```export C_INCLUDE_PATH=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Headers```


# data sources 
https://www.scb.se/en/services/open-data-api/open-geodata/localities/


