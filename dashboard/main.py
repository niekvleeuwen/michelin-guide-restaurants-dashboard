import os

import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from data_loader import load_data
from flask import send_from_directory
from loguru import logger

app = Dash(
    title="Michelin Guide Restaurants Dashboard",
    external_stylesheets=[dbc.icons.BOOTSTRAP],
    use_pages=True,
)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

PAGE_ICON_MAPPING = {
    "Home": "bi bi-house",
    "Countries": "bi bi-globe-americas",
    "About": "bi bi-info-circle",
}

sidebar = html.Div(
    [
        html.Img(src="assets/img/logos/MichelinStar.svg", width=80),
        html.Hr(),
        html.P("Michelin Guide Restaurants Dashboard", className="lead"),
        dbc.Nav([], vertical=True, pills=True, id="sidebar-nav"),
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)

content = html.Div(dash.page_container, style=CONTENT_STYLE)

app.layout = html.Div(
    [
        # Load the data once, and store it in a dcc.Store
        dcc.Store(id="store", data=load_data().to_dict()),
        dcc.Location(id="url"),
        sidebar,
        content,
    ]
)


@app.callback(Output("sidebar-nav", "children"), Input("url", "pathname"))
def update_navbar(url: str) -> list:
    return [
        dcc.Link(
            html.Div(
                [html.I(className=PAGE_ICON_MAPPING[page["name"]] + " mr-1"), page["name"]],
                className="d-flex align-items-center",
            ),
            href=page["relative_path"],
            className="nav-link active" if page["relative_path"] == url else "nav-link",
        )
        for page in dash.page_registry.values()
    ]


# Serve static files
@app.server.route("/static/<path:path>")
def static_file(path):
    static_folder = os.path.join(os.getcwd(), "static")
    return send_from_directory(static_folder, path)


app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        {%css%}
        <link rel="icon" href="assets/img/logos/MichelinStar.svg">
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>

<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,300..900;1,300..900&display=swap');
</style>
"""

if __name__ == "__main__":
    logger.info("Starting server")
    app.run_server(debug=True)
