import pandas as pd
import plotly.express as px
from utils import apply_style_to_fig


def graph_top_cuisine(df: pd.DataFrame, top: int = 10):
    fig_top_cuisines = px.bar(
        df["Cuisine"].value_counts()[:top].reset_index(),
        x="Cuisine",
        y="count",
        labels={"count": "Number of restaurants"},
    )

    fig_top_cuisines = apply_style_to_fig(fig_top_cuisines)
    return fig_top_cuisines
