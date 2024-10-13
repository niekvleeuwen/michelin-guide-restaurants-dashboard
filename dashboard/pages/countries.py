import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html
from data_utils import number_of_cities, number_of_restaurants, top_cuisine
from graphs import graph_top_cuisine
from utils import apply_style_to_fig

dash.register_page(__name__)

layout = [
    html.H3("Countries", className="mb-3"),
    html.P(
        """Visualize data per country.
        """
    ),
    dbc.Row(dbc.Col(dcc.Dropdown([], id="country-dropdown-selection"), width=3), class_name="mt-2"),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(
                                "-",
                                id="countries-number-of-cities",
                                className="card-title",
                            ),
                            html.H6("Number of cities", className="card-subtitle"),
                        ]
                    ),
                )
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(
                                "-",
                                id="countries-number-of-restaurants",
                                className="card-title",
                            ),
                            html.H6("Number of restaurants", className="card-subtitle"),
                        ]
                    ),
                )
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("-", id="countries-top-cuisine", className="card-title"),
                            html.H6("Top cuisine", className="card-subtitle"),
                        ]
                    ),
                )
            ),
        ],
        class_name="mt-4",
    ),
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4("Map"),
                        html.P("A map showing the location of Michelin-starred restaurants."),
                        dcc.Graph(id="countries-map-graph-content"),
                    ]
                )
            )
        ),
        class_name="mt-3",
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Top cities"),
                            html.P("Cities with the most restaurants in the Michelin Guide."),
                            dcc.Graph(
                                id="countries-graph-top-cities",
                            ),
                        ]
                    )
                ),
                width=6,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Top cuisines"),
                            html.P("The most common cuisine types of restaurants in the Michelin Guide."),
                            dcc.Graph(
                                id="countries-graph-top-cuisine",
                            ),
                        ]
                    )
                ),
                width=6,
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
                            html.H4("Award distribution"),
                            html.P("Breakdown of distribution of Michelin ratings."),
                            dcc.Graph(id="countries-awards-distribution"),
                        ]
                    )
                ),
                width=6,
            ),
            dbc.Col(
                dbc.Card(dbc.CardBody([])),
                width=6,
            ),
        ],
        class_name="mt-3",
    ),
]


@callback(
    [
        Output("country-dropdown-selection", "options"),
        Output("country-dropdown-selection", "value"),
    ],
    Input("store", "data"),
)
def update_dropdown(df):
    """Update dropdown with unique countries."""
    df = pd.DataFrame.from_dict(df)

    countries = df[df["Country"].notna()]["Country"].unique()

    return sorted(countries), "France"


@callback(
    [
        Output("countries-number-of-cities", "children"),
        Output("countries-number-of-restaurants", "children"),
        Output("countries-top-cuisine", "children"),
    ],
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
def update_numbers(df_dict: dict, country: str):
    """Callback to update numbers on the top of homepage."""
    df = load_filter_df(df_dict, country)

    return (
        number_of_cities(df),
        number_of_restaurants(df),
        top_cuisine(df),
    )


@callback(
    Output("countries-graph-top-cities", "figure"),
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
def graph_top_countries(df_dict: dict, country: str) -> go.Figure:
    """Graph the top x countries in the dataset."""
    df_top_countries = load_filter_df(df_dict, country)

    fig_top_countries = px.bar(
        df_top_countries["City"].value_counts()[:10].reset_index(),
        x="City",
        y="count",
        labels={"count": "Number of restaurants"},
    )

    fig_top_countries = apply_style_to_fig(fig_top_countries)
    return fig_top_countries


@callback(
    Output("countries-graph-top-cuisine", "figure"),
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
def countries_top_cuisine(df_dict: dict, country: str) -> go.Figure:
    """Graph the top x cuisines in the dataset."""
    df_top_cuisines = load_filter_df(df_dict, country)

    return graph_top_cuisine(df_top_cuisines)


@callback(
    Output("countries-awards-distribution", "figure"),
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
def graph_award_distribution(df_dict: dict, country: str):
    df = load_filter_df(df_dict, country)

    fig = px.bar(
        df["Award"].value_counts().reset_index(),
        x="Award",
        y="count",
        labels={"count": "Number of restaurants"},
    )

    fig = apply_style_to_fig(fig)
    return fig


@callback(
    Output("countries-map-graph-content", "figure"),
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
def update_graph_map(df_dict: pd.DataFrame, country: str):
    """Plot the locations of restaurants on a map."""
    df = load_filter_df(df_dict, country)

    # TODO: add name of restaurant
    fig = px.scatter_map(
        data_frame=df,
        lat="Latitude",
        lon="Longitude",
        color="Award",
        size="Award (Map Size)",
        hover_data={"Award (Map Size)": False},
        zoom=4,
    )
    fig = apply_style_to_fig(fig, apply_trace_color=False)
    return fig


# TODO: convert to decorator
def load_filter_df(df_dict, country: str) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(df_dict)

    df = df[df["Country"] == country]

    return df
