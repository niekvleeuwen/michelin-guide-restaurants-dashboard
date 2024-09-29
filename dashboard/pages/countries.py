import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px


dash.register_page(__name__)


layout = [
    html.H3(children="Countries", style={"textAlign": "center"}),
    dcc.Dropdown([], id="country-dropdown-selection"),
    dcc.Graph(id="graph-content"),
    dcc.Graph(id="country-map-graph-content"),
]


@callback(
    Output("country-dropdown-selection", "options"),
    Input("store", "data"),
)
def update_dropdown(df):
    """Update dropdown with unique countries."""
    df = pd.DataFrame.from_dict(df)

    countries = df[df["Country"].notna()]["Country"].unique()

    return sorted(countries)


@callback(
    Output("graph-content", "figure"),
    Input("store", "data"),
    Input("country-dropdown-selection", "value"),
)
def update_graph(df, value):
    df = pd.DataFrame.from_dict(df)
    df_filtered = df[df["Country"] == value]
    value_counts = df_filtered["Award"].value_counts().reset_index()
    print(value_counts)
    return px.bar(value_counts, x="Award", y="count")


@callback(
    Output("country-map-graph-content", "figure"),
    Input("store", "data"),
    Input("country-dropdown-selection", "value"),
)
def update_graph_map(df, value):
    df = pd.DataFrame.from_dict(df)

    df = df[df["Country"] == value]

    return px.scatter_map(
        data_frame=df,
        lat="Latitude",
        lon="Longitude",
        color="Award",
        size="Award (Map Size)",
        hover_data={"Award (Map Size)": False},
        zoom=4,
    )
