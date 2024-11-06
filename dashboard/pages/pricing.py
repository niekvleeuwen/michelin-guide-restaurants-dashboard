import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

from data.utils import unique_countries
from decorators import df_from_dict, filter_by_country
from graphs.graphs import (
    graph_heatmap_price,
    graph_price_distribution,
    graph_scatter_best_value,
)
from utils import TITLE

PAGE_TITLE = "Pricing"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=2)

layout = [
    html.H3("Pricing", className="mb-3"),
    html.P(
        """This page provides an overview of pricing,
        showcasing the distribution of Michelin Guide restaurants across different price categories.
        """
    ),
    dbc.Row(
        dbc.Col(dcc.Dropdown([], clearable=False, id="pricing-country-dropdown-selection"), width=3), class_name="mt-1"
    ),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Price Distribution"),
                            html.P(" Number of restaurants in each price category."),
                            dcc.Graph(id="pricing-graph-price-distribution"),
                        ]
                    ),
                )
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Heatmap"),
                            html.P("Heatmap of Michelin Award by price category."),
                            dcc.Graph(id="pricing-graph-heatmap"),
                        ]
                    ),
                )
            ),
        ],
        class_name="mt-4",
    ),
    dbc.Row(
        dbc.Col(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Best value"),
                            html.P(
                                [
                                    """This plot shows how Michelin Guide restaurants in different price categories
                                    align with their awards""",
                                    html.Span(
                                        html.I(className="bi bi-info-circle ml-2"),
                                        id="pricing-best-value-tooltip-target",
                                        style={"cursor": "pointer"},
                                    ),
                                    dbc.Tooltip(
                                        """
                                    A higher award at a lower price indicates better value.
                                    """,
                                        target="pricing-best-value-tooltip-target",
                                    ),
                                    ".",
                                ]
                            ),
                            dcc.Graph(id="pricing-best-value-scatter"),
                        ]
                    ),
                )
            ],
            width=12,
        ),
        class_name="mt-4",
    ),
]


@callback(
    [
        Output("pricing-country-dropdown-selection", "options"),
        Output("pricing-country-dropdown-selection", "value"),
    ],
    Input("store", "data"),
)
@df_from_dict
def update_dropdown(df):
    """Update dropdown with unique countries."""
    countries = unique_countries(df)
    default_country = "France"
    return sorted(countries), default_country


@callback(
    Output("pricing-graph-price-distribution", "figure"),
    [
        Input("store", "data"),
        Input("pricing-country-dropdown-selection", "value"),
    ],
)
@df_from_dict
@filter_by_country
def update_price_distribution(df: pd.DataFrame):
    """Update the price distribution graph."""
    return graph_price_distribution(df)


@callback(
    Output("pricing-best-value-scatter", "figure"),
    [
        Input("store", "data"),
        Input("pricing-country-dropdown-selection", "value"),
    ],
)
@df_from_dict
@filter_by_country
def update_graph_scatter_best_value(df: pd.DataFrame):
    """Update the best value graph."""
    return graph_scatter_best_value(df)


@callback(
    Output("pricing-graph-heatmap", "figure"),
    [
        Input("store", "data"),
        Input("pricing-country-dropdown-selection", "value"),
    ],
)
@df_from_dict
@filter_by_country
def update_graph_heatmap_price(df: pd.DataFrame):
    """Update the heatmap graph."""
    return graph_heatmap_price(df)
