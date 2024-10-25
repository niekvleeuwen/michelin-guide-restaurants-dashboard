import dash
from dash import html

from dashboard.utils import TITLE

PAGE_TITLE = "About"

dash.register_page(
    __name__,
    name=PAGE_TITLE,
    title=f"{PAGE_TITLE} | {TITLE}",
)


layout = [
    html.H3("About"),
    html.P(
        [
            "This dashboard is created by ",
            html.A("Niek van Leeuwen", href="https://niekvanleeuwen.nl"),
            ", as part of the Plotly Dash ",
            html.A("Autumn App Challenge 2024", href="https://community.plotly.com/t/autumn-app-challenge/87373"),
            ".",
        ]
    ),
    html.H5("Attributions"),
    html.Ul(
        [
            html.Li(
                [
                    html.B("Michelin logo: "),
                    "Nikolaos Dimos, CC BY-SA 3.0 ",
                    html.A("via Wikimedia Commons", href="https://creativecommons.org/licenses/by-sa/3.0"),
                    ".",
                ],
            ),
            html.Li(
                [
                    html.B("Dataset: "),
                    "Jerry Ng on ",
                    html.A("Kaggle", href="https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021"),
                    ".",
                ],
            ),
        ]
    ),
]
