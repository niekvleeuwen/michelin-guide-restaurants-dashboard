import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from graph_utils import MICHELIN_PRIMARY_COLOR, apply_style_to_fig


def graph_top_countries(df: pd.DataFrame, top: int = 10) -> go.Figure:
    """Graph the top x countries in the dataset."""
    counts = df["Country"].value_counts()[:top].reset_index()
    fig = px.bar(counts, x="Country", y="count", labels={"count": "Number of restaurants"}, text=counts["count"])
    fig.update_traces(textposition="outside")
    fig = apply_style_to_fig(fig)
    return fig


def graph_top_cities(df: pd.DataFrame, top: int = 10) -> go.Figure:
    """Graph the top x cities in the dataset."""
    counts = df["City"].value_counts()[:top].reset_index()
    fig = px.bar(counts, x="City", y="count", labels={"count": "Number of restaurants"}, text=counts["count"])
    fig.update_traces(textposition="outside")
    fig = apply_style_to_fig(fig)
    return fig


def graph_top_cuisine(df: pd.DataFrame, top: int = 10) -> go.Figure:
    """Graph top x cuisines in the dataset."""
    counts = df["Cuisine"].value_counts()[:top].reset_index()
    fig = px.bar(counts, x="Cuisine", y="count", labels={"count": "Number of restaurants"}, text=counts["count"])
    fig.update_traces(textposition="outside")

    fig = apply_style_to_fig(fig)
    return fig


def graph_award_distribution(df: pd.DataFrame) -> go.Figure:
    """Graph the distribution of the award column."""
    counts = df["Award"].value_counts().reset_index()
    fig = px.bar(counts, x="Award", y="count", labels={"count": "Number of restaurants"}, text=counts["count"])
    fig.update_traces(textposition="outside")

    fig = apply_style_to_fig(fig)
    return fig


def graph_green_star_distribution(df: pd.DataFrame) -> go.Figure:
    """Graph the distribution of the Green Star."""
    df["GreenStar"] = df["GreenStar"].map({True: "Awarded", False: "Not awarded"})

    counts = df["GreenStar"].value_counts()

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=counts.index, values=counts, hole=0.5)])
    fig.update_traces(marker=dict(colors=[MICHELIN_PRIMARY_COLOR, "#23BDAD"]))
    return fig


def graph_map(df: pd.DataFrame) -> go.Figure:
    """Create a map with all restaurants (size based on award)."""
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


def graph_price_distribution(df: pd.DataFrame, normalized_values: bool = False) -> go.Figure:
    """Graph the price distribution."""
    counts = df["Price"].value_counts().reset_index()
    fig = px.bar(counts, x="Price", y="count", labels={"count": "Number of restaurants"}, text=counts["count"])
    fig.update_xaxes(categoryorder="category ascending")
    fig.update_traces(textposition="outside")

    fig = apply_style_to_fig(fig)
    return fig


def graph_price_distribution_normalized(df: pd.DataFrame) -> go.Figure:
    """Graph the price distribution."""
    col = "Price (normalized)"
    counts = df[col].value_counts().reset_index()
    fig = px.bar(
        counts,
        x=col,
        y="count",
        labels={"count": "Number of restaurants"},
        category_orders={"Price (normalized)": ["Budget-Friendly", "Moderate", "Premium", "Luxury"]},
        text=counts["count"],
    )
    fig.update_traces(textposition="outside")

    fig = apply_style_to_fig(fig)
    return fig
