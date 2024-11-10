import dash
import dash_bootstrap_components as dbc
from caching import retrieve_data
from dash import dcc, html
from data.utils import number_of_countries, number_of_restaurants, top_cuisine
from graphs.graphs import (
    graph_award_distribution,
    graph_green_star_distribution,
    graph_price_distribution_normalized,
    graph_top_cities,
    graph_top_countries,
    graph_top_cuisine,
)
from utils import TITLE

PAGE_TITLE = "Overview"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/", order=0)


def layout():
    df = retrieve_data()
    return [
        html.H3("Overview", className="mb-3"),
        html.P(
            """The Michelin Guide has long been synonymous with culinary excellence,
        serving as a global benchmark for top-tier dining experiences. This dashboard explores
        the data from this guide, to provide insights and maybe make a recommendation or two!
        """
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    number_of_countries(df),
                                    id="home-number-of-countries",
                                    className="card-title",
                                ),
                                html.H6("Number of countries", className="card-subtitle"),
                            ]
                        ),
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    number_of_restaurants(df),
                                    id="home-number-of-restaurants",
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
                                html.H4(top_cuisine(df), id="home-top-cuisine", className="card-title"),
                                html.H6("Top cuisine", className="card-subtitle"),
                            ]
                        ),
                    )
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Award distribution"),
                                html.P("Distribution of Michelin ratings."),
                                dcc.Graph(id="home-awards-distribution", figure=graph_award_distribution(df)),
                            ]
                        ),
                        class_name="h-100",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Green Star distribution"),
                                html.P("""
                                The Green Star of Michelin recognizes restaurants for their commitment to sustainability
                                and environmentally friendly practices.
                            """),
                                dcc.Graph(id="home-green-star-distribution", figure=graph_green_star_distribution(df)),
                            ]
                        ),
                        class_name="h-100",
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
                                html.H4("Top cuisines"),
                                html.P("The most common cuisine types of restaurants in the Michelin Guide."),
                                dcc.Graph(id="home-graph-top-cuisine", figure=graph_top_cuisine(df)),
                            ]
                        ),
                        class_name="h-100",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Price Distribution"),
                                html.P(
                                    """Number of restaurants in each price category. This data is normalized across
                                currencies."""
                                ),
                                dcc.Graph(
                                    id="home-graph-price-distribution", figure=graph_price_distribution_normalized(df)
                                ),
                            ]
                        ),
                        class_name="h-100",
                    ),
                    width=6,
                ),
            ],
            class_name="mt-3",
        ),
        html.H5("Locations", className="mt-3 mb-2"),
        html.P(
            """This section highlights the top countries and locations with Michelin Guide restaurants,
        showcasing key insights into their global distribution
        """
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Top countries"),
                                html.P("Countries with the most restaurants in the Michelin Guide."),
                                dcc.Graph(id="home-graph-top-countries", figure=graph_top_countries(df)),
                            ]
                        ),
                        class_name="h-100",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Top cities"),
                                html.P("Cities with the most restaurants in the Michelin Guide."),
                                dcc.Graph(id="home-graph-top-cities", figure=graph_top_cities(df)),
                            ]
                        ),
                        class_name="h-100",
                    ),
                    width=6,
                ),
            ],
            class_name="mt-3",
        ),
    ]
