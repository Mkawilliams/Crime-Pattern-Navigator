import json
import sqlite3

# This script connects to the SQLite database, creates a table for police subdivisions,
# loads the geographical polygons from a GeoJSON file, and inserts the data into the database.
# connect to database
conn = sqlite3.connect("crime.db")
cur = conn.cursor()

# Create table
cur.execute("""CREATE TABLE subdivision (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    geom TEXT
)""")

# Load GeoJSON data
with open("backend/geo/Police Subdivisions.geojson") as f:
    data = json.load(f)

# Insert data into database
for feature in data["features"]:
    name = feature["properties"].get("Name", "Unknown")
    geom = json.dumps(feature["geometry"])

    cur.execute("INSERT INTO subdivision (name, geom) VALUES (?, ?)", (name, geom))
# Commit changes and close connection
conn.commit()
conn.close()

print("GeoJSON data loaded into database successfully.")
