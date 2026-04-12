from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import os
import pandas as pd

# This script sets up a FastAPI application that serves crime data from a SQLite database.
# It provides endpoints for retrieving filter options, map data, and table data based on user-selected criteria.
# The application also handles CORS to allow requests from a frontend running on localhost:3000.
# The crime data is loaded into a DataFrame for efficient querying and filtering before being returned as JSON responses.

# Initialize FastAPI app
app = FastAPI()

# Connect to the SQLite database and load the data into a DataFrame
conn = sqlite3.connect("crime.db", check_same_thread=False)
df = pd.read_sql_query("SELECT * FROM crime_data", conn)

# Load GeoJSON properly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "geo", "police_subdivisions.geojson")) as f:
    geojson = json.load(f)

# Define division_lookup mapping
division_lookup = {
    feature["properties"]["Code"]: feature["properties"]["Name"]
    for feature in geojson["features"]
}
df["division_name"] = df["division_code"].map(division_lookup)


# Opening Message
@app.get("/")
def read_root():
    return {"message": "Welcome to the Bahamas Crime Data API!"}


# Filter Options
@app.get("/filters")
def get_filters():
    return {
        "years": sorted(df["Year"].unique().tolist()),
        "divisions": sorted(df["division_name"].unique().tolist()),
        "offences": sorted(df["Offence"].unique().tolist()),
    }


# Map Data
@app.get("/map-data")
def get_map_data(
    years: list[int] = Query(None),
    divisions: list[str] = Query(None),
    offences: list[str] = Query(None),
):
    filtered = df.copy()
    if years:
        filtered = filtered[filtered["Year"].isin(years)]
    if divisions:
        filtered = filtered[filtered["division_name"].isin(divisions)]
    if offences:
        filtered = filtered[filtered["Offence"].isin(offences)]

    # Group for Map
    grouped = filtered.groupby("division_name")["crime_count"].sum().reset_index()
    return grouped.to_dict(orient="records")


# Table Data
@app.get("/table-data")
def get_table_data(
    years: list[int] = Query(None),
    divisions: list[str] = Query(None),
    offences: list[str] = Query(None),
):
    print("Filters received:", years, divisions, offences)

    # Apply filters to the DataFrame
    filtered = df.copy()
    if years:
        filtered = filtered[filtered["Year"].isin(years)]
    if divisions:
        filtered = filtered[filtered["division_name"].isin(divisions)]
    if offences:
        filtered = filtered[filtered["Offence"].isin(offences)]

    # Group for Table
    grouped = (
        filtered.groupby(["Year", "division_name", "Offence"])["crime_count"]
        .sum()
        .reset_index()
        .sort_values(by="crime_count", ascending=False)
    )
    return grouped.to_dict(orient="records")


# Set up CORS middleware to allow requests from the frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
