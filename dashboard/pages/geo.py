import dash
import dash_bootstrap_components as dbc
import pandas as pd
from caching import retrieve_data
from dash import Input, Output, callback, dcc, html
from decorators import load_df
from graphs.graphs import graph_green_star_map, graph_map_cuisine
from utils import TITLE

PAGE_TITLE = "Geospatial Analysis"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/geo", order=0)


def layout():
    df = retrieve_data()
    return [
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
                                    id="cuisine-dropdown",
                                    options=construct_cuisine_dropdown(df),
                                    placeholder="Select a cuisine type",
                                    className="my-2",
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
                                dcc.Graph(id="green-star-map", figure=graph_green_star_map(df)),
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


def construct_cuisine_dropdown(df: pd.DataFrame) -> list[str]:
    """Construct a list with options for the cuisine dropdown."""
    cuisine_options = []
    cuisines = df[df["Cuisine"].notna()]["Cuisine"].unique().tolist()
    for cuisine in cuisines:
        cuisine_options += cuisine.split(", ")

    return sorted(list(set(cuisine_options)))


@callback(Output("cuisine-map", "figure"), Input("cuisine-dropdown", "value"))
@load_df
def display_cuisine_map(df, selected_cuisine):
    if selected_cuisine:
        filtered_df = df[df["Cuisine"] == selected_cuisine]
    else:
        filtered_df = df  # Show all if no selection

    return graph_map_cuisine(filtered_df)
