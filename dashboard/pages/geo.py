import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

from dashboard.decorators import df_from_dict
from dashboard.graphs.graphs import graph_green_star_map, graph_map_cuisine
from dashboard.utils import TITLE

PAGE_TITLE = "Geospatial Analysis"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/geo", order=0)

layout = [
    html.H3(PAGE_TITLE, className="mb-3"),
    html.P(
        """Analysis of geolocation data provided by Michelin.
        """
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Cuisine"),
                            html.P("""
                                This map allows you to select a specific cuisine type from a dropdown.
                            """),
                            dcc.Dropdown(
                                id="cuisine-dropdown", options=[], placeholder="Select a Cuisine Type", className="my-2"
                            ),
                            dcc.Graph(id="cuisine-map"),
                        ]
                    ),
                    class_name="h-100",
                ),
                width=12,
            ),
        ],
        class_name="mt-3",
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Green Star distribution"),
                            html.P("""
                                The Green Star of Michelin recognizes restaurants for their commitment to sustainability
                                and environmentally friendly practices.
                            """),
                            dcc.Graph(id="green-star-map"),
                        ]
                    ),
                    class_name="h-100",
                ),
                width=12,
            ),
        ],
        class_name="mt-3",
    ),
]


@callback(
    Output("cuisine-dropdown", "options"),
    Input("store", "data"),
)
@df_from_dict
def fill_cuisines(df):
    cuisine_options = []
    cuisines = df[df["Cuisine"].notna()]["Cuisine"].unique().tolist()
    for cuisine in cuisines:
        cuisine_options += cuisine.split(", ")

    return sorted(list(set(cuisine_options)))


@callback(Output("cuisine-map", "figure"), Input("store", "data"), Input("cuisine-dropdown", "value"))
@df_from_dict
def display_cuisine_map(df, selected_cuisine):
    if selected_cuisine:
        filtered_df = df[df["Cuisine"] == selected_cuisine]
    else:
        filtered_df = df  # Show all if no selection

    return graph_map_cuisine(filtered_df)


@callback(
    Output("green-star-map", "figure"),
    [
        Input("store", "data"),
    ],
)
@df_from_dict
def display_green_star_map(df: pd.DataFrame):
    green_star_df = df[df["GreenStar"] == 1]
    return graph_green_star_map(green_star_df)
