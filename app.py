import sqlite3
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import json
import os

# Load crime data from SQLite database
conn = sqlite3.connect("crime.db")
df = pd.read_sql_query("SELECT * FROM crime_data", conn)

# Load GeoJSON properly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "geo", "police_subdivisions.geojson")) as f:
    geojson = json.load(f)

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div(
    [
        # Fullscreen Map
        dcc.Graph(
            id="crime_map",
            style={"height": "100vh"},
            config={
                "displayModeBar": False,
                "scrollZoom": True,
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
                ),
                dcc.Dropdown(
                    id="division_filter",
                    options=[
                        {"label": d, "value": d}
                        for d in sorted(df["division_code"].unique())
                    ],
                    multi=True,
                    placeholder="Division",
                ),
                dcc.Dropdown(
                    id="offence_filter",
                    options=[
                        {"label": o, "value": o} for o in sorted(df["Offence"].unique())
                    ],
                    multi=True,
                    placeholder="Offence",
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
                ),
            ],
            style={
                "position": "absolute",
                "top": "20px",
                "left": "20px",
                "zIndex": 1000,
                "background": "rgba(0,0,0,0.6)",
                "color": "black",
                "padding": "15px",
                "borderRadius": "12px",
                "width": "260px",
                "boxShadow": "0 8px 20px rgba(0,0,0,0.4)",
                "opacity": 0.5,
            },
        ),
        # Title Overlay
        html.Div(
            "Bahamas Crime Intelligence Map",
            style={
                "position": "absolute",
                "top": "20px",
                "right": "200px",
                "zIndex": 1000,
                "background": "rgba(0,0,0,0.6)",
                "color": "white",
                "padding": "10px 15px",
                "borderRadius": "8px",
                "fontWeight": "bold",
            },
        ),
    ]
)


# Callback to update the map based on filters
@app.callback(
    Output("crime_map", "figure"),
    Input("year_filter", "value"),
    Input("division_filter", "value"),
    Input("offence_filter", "value"),
    Input("map_style", "value"),
)
def update_map(years, divisions, offences, map_style):

    filtered = df.copy()

    if years:
        filtered = filtered[filtered["Year"].isin(years)]

    if divisions:
        filtered = filtered[filtered["division_code"].isin(divisions)]

    if offences:
        filtered = filtered[filtered["Offence"].isin(offences)]

    grouped = filtered.groupby("division_code")["crime_count"].sum().reset_index()

    fig = px.choropleth_mapbox(
        grouped,
        geojson=geojson,
        locations="division_code",
        featureidkey="properties.Code",
        color="crime_count",
        color_continuous_scale="Reds",
        mapbox_style=map_style,
        center={"lat": 25.05, "lon": -77.35},
        zoom=10,
        opacity=0.75,
    )

    fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    uirevision="constant",

    mapbox=dict(
        center={"lat": 25.05, "lon": -77.35},
        zoom=10
    ),

    coloraxis_colorbar=dict(
        thickness=8,
        len=0.35,
        y=0.5
    )
)
    
    return fig


if __name__ == "__main__":
    app.run(debug=True)
