import sqlite3
import webbrowser
import pandas as pd
import json
import folium

# Used in initial protoype to create a crime map. T
# This script connects to the SQLite database, queries the total crime count by division,
# loads the geographical polygons for the police subdivisions,
# And creates a choropleth map using Folium. The map is saved as an HTML file and opened in the default web browser.

# Connect to database
conn = sqlite3.connect("crime.db")

# Query crime totals by division
df = pd.read_sql_query(
    """
SELECT division_code, SUM(crime_count) as crime_count
FROM crime_data
GROUP BY division_code
""",
    conn,
)

# load polygons
with open("backend/geo/Police Subdivisions.geojson") as f:
    geo = json.load(f)

# Create map
crime_map = folium.Map(
    location=[25.05, -77.35],
    zoom_start=12,
)

folium.Choropleth(
    geo_data=geo,
    data=df,
    columns=["division_code", "crime_count"],
    key_on="feature.properties.Code",
    fill_color="Reds",
    fill_opacity=0.8,
    line_opacity=0.4,
    line_color="black",
    line_weight=2,
    legend_name="Total Crime by Division",
).add_to(crime_map)

# Add tooltips to show division name and crime count on hover
folium.GeoJson(
    geo,
    name="Divisions",
    tooltip=folium.GeoJsonTooltip(
        fields=["Name", "Code"], aliases=["Division:", "Code:"], localize=True
    ),
).add_to(crime_map)

# Save map to HTML and open in browser
crime_map.save("crime_map.html")

print("Map created successfully")

webbrowser.open("crime_map.html")
