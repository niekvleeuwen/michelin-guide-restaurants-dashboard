import dash
from dash import html


dash.register_page(__name__)

layout = [
    html.H3("About"),
    html.P(
        [
            "This dashboard is created by ",
            html.A("Niek van Leeuwen", href="https://niekvanleeuwen.nl"),
            ", as part of the Plotly Dash ",
            html.A("Autumn App Challenge", href="https://community.plotly.com/t/autumn-app-challenge/87373"),
            ".",
        ]
    ),
    html.H5("Attributions"),
    html.P(
        [
            html.B("Michelin logo: "),
            "Nikolaos Dimos, CC BY-SA 3.0 ",
            html.A("via Wikimedia Commons", href="https://creativecommons.org/licenses/by-sa/3.0"),
            ".",
        ]
    ),
]
