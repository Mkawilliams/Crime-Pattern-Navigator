import sqlite3
import pandas as pd
import plotly.express as px
import json
import os
import plotly.graph_objects as go
from dash import Dash, ctx, dcc, html
from dash.dependencies import Input, Output

# Used in the initial prototype but not currently in use. Keeping for potential future use.
# This app is a Dash-based interactive map that visualizes crime data across police subdivisions in the Bahamas.
# It allows users to filter crime data by year, division, and offence type, and displays the results on a choropleth map.
# The app also includes a summary table that updates based on the selected filters and clicked division on the map.

# Load crime data from SQLite database
conn = sqlite3.connect("crime.db")
df = pd.read_sql_query("SELECT * FROM crime_data", conn)

# Load GeoJSON properly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "geo", "police_subdivisions.geojson")) as f:
    geojson = json.load(f)

# Look up division names for hover info
division_lookup = {
    feature["properties"]["Code"]: feature["properties"]["Name"]
    for feature in geojson["features"]
}

# Initialize Dash app
app = Dash(__name__)

# Define app layout with map and filters
app.layout = html.Div(
    className="app-container",
    children=[
        # Disclaimer banner
        html.Div(
            "Disclaimer: This map is for research and educational purposes only. It is not an official government product. Data is sourced from public RBPF's reports.",
            className="disclaimer",
            style={
                "background": "rgba(255,0,0,0.8)",
                "color": "white",
                "padding": "10px",
                "textAlign": "center",
                "fontWeight": "bold",
                "boxSizing": "border-box",
            },
        ),
        # Title Overlay
        html.Div(
            "Bahamas Crime Intelligence Map",
            className="title-overlay",
            style={
                "background": "rgba(0,0,0,0.6)",
                "color": "white",
                "padding": "10px 15px",
                "borderRadius": "8px",
                "fontWeight": "bold",
                "boxSizing": "border-box",
            },
        ),
        # Overlay Filters
        html.Div(
            [
                dcc.Dropdown(
                    id="year_filter",
                    options=[
                        {"label": y, "value": y} for y in sorted(df["Year"].unique())
                    ],
                    value=[df["Year"].max()],
                    multi=True,
                    placeholder="Year",
                    clearable=False,
                ),
                dcc.Dropdown(
                    id="division_filter",
                    options=[
                        {"label": division_lookup.get(code, code), "value": code}
                        for code in sorted(df["division_code"].unique())
                    ],
                    multi=True,
                    placeholder="Division",
                    clearable=False,
                    style={"marginTop": "8px"},
                ),
                dcc.Dropdown(
                    id="offence_filter",
                    options=[
                        {"label": o, "value": o} for o in sorted(df["Offence"].unique())
                    ],
                    multi=True,
                    placeholder="Offence",
                    clearable=True,
                    style={"marginTop": "8px"},
                ),
                # Map style toggle
                dcc.RadioItems(
                    id="map_style",
                    options=[
                        {"label": "Dark", "value": "carto-darkmatter"},
                        {"label": "Light", "value": "carto-positron"},
                    ],
                    value="carto-positron",
                    style={"marginTop": "10px"},
                    inputStyle={"marginRight": "5px"},
                ),
            ],
            # Filter container styling for better visibility and user experience
            className="filters",
            style={
                "position": "absolute",
                "top": "40px",
                "left": "20px",
                "zIndex": 1000,
                "background": "rgba(0,0,0,0.6)",
                "color": "black",
                "padding": "15px",
                "borderRadius": "12px",
                "width": "260px",
                "boxShadow": "0 8px 20px rgba(0,0,0,0.4)",
                "opacity": 0.5,
                "boxSizing": "border-box",
            },
        ),
        # Fullscreen Map
        html.Div(
            dcc.Graph(
                id="crime_map",
                className="crime-map",
                style={"height": "100vh"},
                config={
                    "displayModeBar": False,
                    "scrollZoom": True,
                },
            ),
            className="map-wrapper",
            style={"position": "relative", "width": "100%", "height": "100vh"},
        ),
        # Summary Table Overlay
        html.Div(
            children=[
                dcc.Graph(
                    id="summary_table",
                    className="summary-table",
                    style={
                        "position": "absolute",
                        "bottom": "140px",
                        "right": "20px",
                        "zIndex": 1000,
                        "background": "rgba(0,0,0,0.6)",
                        "padding": "10px",
                        "width": "25%",
                        "borderRadius": "8px",
                        "overflowY": "auto",
                        "opacity": 0.9,
                        "boxSizing": "border-box",
                    },
                ),
                # Right corner copyright notice
                html.Div(
                    "©️ 2026 Matthew Williams. All rights reserved.",
                    style={
                        "position": "fixed",
                        "bottom": "10px",
                        "right": "20px",
                        "color": "white",
                        "background": "rgba(0,0,0,0.6)",
                        "padding": "5px 10px",
                        "borderRadius": "8px",
                        "fontSize": "12px",
                        "zIndex": 3000,
                    },
                ),
            ],
            className="table-wrapper",
        ),
    ],
)

# Map division codes to names for hover info
df["division_name"] = df["division_code"].map(division_lookup)


# Callback to update the map based on filters
@app.callback(
    Output("crime_map", "figure"),
    Input("year_filter", "value"),
    Input("division_filter", "value"),
    Input("offence_filter", "value"),
    Input("map_style", "value"),
)

# This callback updates the choropleth map based on the selected filters for year, division, offence, and map style.
def update_map(years, divisions, offences, map_style):

    filtered = df.copy()

    if years:
        filtered = filtered[filtered["Year"].isin(years)]

    if divisions:
        filtered = filtered[filtered["division_code"].isin(divisions)]

    if offences:
        filtered = filtered[filtered["Offence"].isin(offences)]

    # Group data by division to get total crime count for coloring the map
    grouped = (
        filtered.groupby(["division_code", "division_name"])["crime_count"]
        .sum()
        .reset_index()
    )

    # Create choropleth map using Plotly Express
    fig = px.choropleth_mapbox(
        grouped,
        geojson=geojson,
        locations="division_code",
        featureidkey="properties.Code",
        color="crime_count",
        color_continuous_scale="Reds",
        hover_name="division_name",
        hover_data={"crime_count": True, "division_code": False},
        custom_data=["division_code"],
        mapbox_style=map_style,
        center={"lat": 25.05, "lon": -77.35},
        zoom=9,
        opacity=0.75,
    )

    # Update layout for better aesthetics and interactivity
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        uirevision="constant",
        mapbox=dict(bearing=0, pitch=0),
        coloraxis_colorbar=dict(
            title=" ",
            orientation="h",
            tickfont=dict(color="red"),
            thickness=8,
            len=0.35,
            y=0.1,
            yanchor="bottom",
            x=0.5,
        ),
    )
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>%{z}<extra></extra>")
    return fig


# Callback to update the comparison table based on filters & Clicked division
@app.callback(
    Output("summary_table", "figure"),
    Input("year_filter", "value"),
    Input("division_filter", "value"),
    Input("offence_filter", "value"),
    Input("crime_map", "clickData"),
)

# This callback generates a summary table of crime counts by year, division, and offence based on the current filters. It groups the data and formats it for display in the DataTable.
def update_table(years, divisions, offences, clickData):
    dff = df.copy()
    if years:
        dff = dff[dff["Year"].isin(years)]
    if divisions:
        dff = dff[dff["division_code"].isin(divisions)]
    if offences:
        dff = dff[dff["Offence"].isin(offences)]

    dff["division_name"] = dff["division_code"].map(division_lookup)

    triggered = [t["prop_id"] for t in ctx.triggered]
    if "crime_map.clickData" in triggered and clickData:
        division_code = clickData["points"][0]["customdata"][0]
        dff = dff[dff["division_code"] == division_code]

    # Group and summarize data for the table
    summary = (
        dff.groupby(["Year", "division_name", "Offence"])
        .sum()
        .reset_index()
        .rename(columns={"division_name": "Division", "crime_count": "Crime Count"})
    )

    # Dynamic height calculation based on number of rows (max 10 rows visible without scroll)
    row_height = 15
    base_height = 35
    total_height = min(
        len(summary) * row_height + base_height, 400
    )  # Max height of 400px

    # Build Plotly table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[
                        "Year",
                        "Division",
                        "Offence",
                        "Crime Count",
                    ],
                    fill_color="lightgrey",
                    font=dict(color="black", size=10),
                    align="center",
                ),
                cells=dict(
                    values=[
                        summary["Year"],
                        summary["Division"],
                        summary["Offence"],
                        summary["Crime Count"],
                    ],
                    font=dict(color="black", size=9),
                    fill_color="lightgrey",
                    align="left",
                ),
            )
        ]
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=total_height,
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
