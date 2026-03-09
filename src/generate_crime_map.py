import sqlite3
import webbrowser
import pandas as pd
import json
import folium

# connect to database
conn = sqlite3.connect("crime.db")

# query crime totals by division
df = pd.read_sql_query(
    """
SELECT division_code, SUM(crime_count) as crime_count
FROM crime_data
GROUP BY division_code
""",
    conn,
)

# load polygons
with open("geo/Police Subdivisions.geojson") as f:
    geo = json.load(f)

# create map
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

folium.GeoJson(
    geo,
    name="Divisions",
    tooltip=folium.GeoJsonTooltip(
        fields=["Name", "Code"], aliases=["Division:", "Code:"], localize=True
    ),
).add_to(crime_map)


crime_map.save("crime_map.html")

print("Map created successfully")

webbrowser.open("crime_map.html")
