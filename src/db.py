#%%
import psycopg2
import dotenv 
import os
from shapely.wkt import loads
from shapely import wkb
import geopandas as gpd

dotenv.load_dotenv()


class Database:
    def __init__(self):
        print('connecting to default database ...')
        self._conn = psycopg2.connect(database='geospatial', user='osmone' , password=os.environ['db_pass'], host='localhost')
        self._cursor = self._conn.cursor()

        print('connected to db ' )


    def get_bus_stops(self):
        query = "SELECT name, ST_AsBinary(way) FROM planet_osm_point WHERE highway='bus_stop'"
        self._cursor.execute(query)
        results = self._cursor.fetchall()

        stops = {}

        for result in results:
            stops[result[0]] = wkb.loads(result[1].hex(), hex=True).wkt # translate binary to shapely geometry

        # geodataframe of bus stops loading the geometry from the wkt and setting the crs to EPSG:900913
        gdf_stops = gpd.GeoDataFrame.from_dict(stops, orient='index', columns=['geometry'])
        gdf_stops['geometry'] = gdf_stops['geometry'].apply(loads)# load the geometry from the wkt
        gdf_stops.crs = "EPSG:900913" # set crs to EPSG:900913
        gdf_stops = gdf_stops.reset_index().rename(columns={'index':'name'}).to_crs("EPSG:4326")# reset index and rename column


        return gdf_stops
    
    def get_bus_routes(self):
        query = "select ref,  ST_AsBinary(way) from planet_osm_line where route = 'bus'"
        self._cursor.execute(query)
        results = self._cursor.fetchall()

        routes = {}

        for res in results:

            routes[res[0]] = wkb.loads(res[1].hex(), hex=True).wkt # translate binary to shapely geometry
                


        gdf_routes = gpd.GeoDataFrame.from_dict(routes, orient='index', columns=['geometry'])
        gdf_routes['geometry'] = gdf_routes['geometry'].apply(loads)# load the geometry from the wkt
        gdf_routes.crs = "EPSG:900913"# set crs to EPSG:900913
        gdf_routes = gdf_routes.reset_index().rename(columns={'index':'ref'}).to_crs("EPSG:4326")# reset index and rename column 
        gdf_routes = gdf_routes[~gdf_routes['ref'].str.contains('[a-zA-Z]')].astype({'ref': 'int32'}).query('ref < 34') # remove values in ref that contains character 

        return gdf_routes

    def get_supermarkets(self):
        query = "SELECT name, ST_AsBinary(way) FROM planet_osm_point WHERE shop='supermarket'"
        self._cursor.execute(query)
        results = self._cursor.fetchall()

        supermarket = {}

        for result in results:
            supermarket[result[0]] = wkb.loads(result[1].hex(), hex=True).wkt # translate binary to shapely geometry

        # geodataframe of bus stops loading the geometry from the wkt and setting the crs to EPSG:900913
        gdf = gpd.GeoDataFrame.from_dict(supermarket, orient='index', columns=['geometry'])
        gdf['geometry'] = gdf['geometry'].apply(loads)# load the geometry from the wkt
        gdf.crs = "EPSG:900913" # set crs to EPSG:900913
        gdf = gdf.reset_index().rename(columns={'index':'name'}).to_crs("EPSG:4326")# reset index and rename column

        return gdf


    def query(self, query):
        try:
            print(f'Executing query: {query}')
            self._cursor.execute(query)
            print(f'Fetching results...')
            results = self._cursor.fetchall()
            print(f'Got {len(results)} results')
            return results
        except Exception as e:
            print(f'Error executing query: {e}')
            return None


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._conn.close()
    


# %%
