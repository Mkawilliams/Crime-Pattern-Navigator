import sqlite3
import pandas as pd
from dash import Dash, ctx, dash_table, dcc, html
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

# Look up division names for hover info
division_lookup = {
    feature["properties"]["Code"]: feature["properties"]["Name"]
    for feature in geojson["features"]
}

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
                        {"label": division_lookup.get(code, code), "value": code}
                        for code in sorted(df["division_code"].unique())
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
            },
        ),
        # Title Overlay
        html.Div(
            "Bahamas Crime Intelligence Map",
            style={
                "position": "absolute",
                "top": "40px",
                "right": "20px",
                "zIndex": 1000,
                "background": "rgba(0,0,0,0.6)",
                "color": "white",
                "padding": "10px 15px",
                "borderRadius": "8px",
                "fontWeight": "bold",
            },
        ),
        # Right corner copyright notice
        html.Div(
            "©️ 2026 Matthew Williams. All rights reserved.",
            style={
                "position": "absolute",
                "bottom": "10px",
                "right": "20px",
                "color": "white",
                "background": "rgba(0,0,0,0.6)",
                "padding": "5px 10px",
                "borderRadius": "8px",
                "fontSize": "12px",
            },
        ),
        html.Div(
            "Disclaimer: This map is for research and educational purposes only. It is not an official government product. Data is sourced from public RBPF's reports.",
            style={
                "position": "absolute",
                "top": "0",
                "left": "0",
                "width": "100%",
                "background": "rgba(255,0,0,0.8)",
                "color": "white",
                "padding": "10px",
                "textAlign": "center",
                "fontWeight": "bold",
                "zIndex": 2000,
            },
        ),
        dash_table.DataTable(
            id="comparison_table",
            columns=[],
            data=[],
            style_table={
                "position": "absolute",
                "top": "120px",
                "right": "20px",
                "width": "300px",
                "maxHeight": "80vh",
                "overflowY": "auto",
            },
            style_cell={
                "backgroundColor": "rgba(255,255,255,0.8)",
                "color": "black",
                "textAlign": "left",
                "padding": "5px",
                "fontFamily": "Arial, sans-serif",
            },
            style_header={
                "backgroundColor": "#111",
                "color": "white",
                "fontWeight": "bold",
            },
        ),
    ]
)


df["division_name"] = df["division_code"].map(division_lookup)


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

    grouped = (
        filtered.groupby(["division_code", "division_name"])["crime_count"]
        .sum()
        .reset_index()
    )

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
    Output("comparison_table", "columns"),
    Output("comparison_table", "data"),
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

    summary = (
        dff.groupby(["Year", "division_name", "Offence"])
        .size()
        .reset_index(name="Crime Count")
    )

    columns = [{"name": col, "id": col} for col in summary.columns]
    data = summary.to_dict("records")
    return columns, data


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
