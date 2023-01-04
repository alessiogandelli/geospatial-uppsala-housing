#%%
from shapely.wkt import loads
import geopandas as gpd
from db import Database


db = Database()
routes = db.get_bus_routes()
stops = db.get_bus_stops()
#%%
# geodataframe of bus stops loading the geometry from the wkt and setting the crs to EPSG:900913
gdf_stops = gpd.GeoDataFrame.from_dict(stops, orient='index', columns=['geometry'])
gdf_stops['geometry'] = gdf_stops['geometry'].apply(loads)# load the geometry from the wkt
gdf_stops.crs = "EPSG:900913" # set crs to EPSG:900913
gdf_stops = gdf_stops.reset_index().rename(columns={'index':'name'}).to_crs("EPSG:4326")# reset index and rename column


# geodataframe of bus routes
gdf_routes = gpd.GeoDataFrame.from_dict(routes, orient='index', columns=['geometry'])
gdf_routes['geometry'] = gdf_routes['geometry'].apply(loads)# load the geometry from the wkt
gdf_routes.crs = "EPSG:900913"# set crs to EPSG:900913
gdf_routes = gdf_routes.reset_index().rename(columns={'index':'ref'}).to_crs("EPSG:4326")# reset index and rename column 
gdf_routes = gdf_routes[~gdf_routes['ref'].str.contains('[a-zA-Z]')].astype({'ref': 'int32'}).query('ref < 34') # remove values in ref that contains character 

#%%


# %%
