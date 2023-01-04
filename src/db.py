#%%
import psycopg2
import dotenv 
import os
dotenv.load_dotenv()

# Connect to the database
conn = psycopg2.connect(database='geospatial', user='osmone' , password=os.environ['db_pass'], host='localhost')

# Create a cursor
cur = conn.cursor()

# Execute a SQL query to retrieve the OSM data
query = "SELECT * FROM planet_osm_point"
cur.execute(query)

# Fetch the results of the query
results = cur.fetchall()

# Print the results
for result in results:
    print(result)

# Close the cursor and connection
cur.close()
conn.close()
# %%
