import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from graphs.utils import apply_style_to_fig
from utils import MICHELIN_PRIMARY_COLOR

MICHELIN_AWARDS_ORDERED = ["Selected Restaurants", "Bib Gourmand", "1 Star", "2 Stars", "3 Stars"]
PRICE_ORDERED = ["Budget-Friendly", "Moderate", "Premium", "Luxury"]


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
    fig = px.scatter_map(
        data_frame=df,
        lat="Latitude",
        lon="Longitude",
        color="Award",
        size="Award (Map Size)",
        hover_data={
            "Award (Map Size)": False,
            "Latitude": False,
            "Longitude": False,
            "Name": True,
            "Location": True,
            "Price": True,
        },
        zoom=4,
    )
    fig = apply_style_to_fig(fig, apply_trace_color=False)
    return fig


def graph_map_cuisine(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Name",
        hover_data={"Award": True, "Price": True, "Location": True, "Latitude": False, "Longitude": False},
        color="Award",
        color_discrete_sequence=px.colors.qualitative.Dark24,
        zoom=3,
        height=700,
    )
    fig = apply_style_to_fig(fig, apply_trace_color=False)
    return fig


def graph_green_star_map(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Name",
        hover_data={"Cuisine": True, "Location": True, "Price": True, "Latitude": False, "Longitude": False},
        color_discrete_sequence=["green"],  # Green for Green Star
        zoom=3,
        height=700,
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
        category_orders={"Price (normalized)": PRICE_ORDERED},
        text=counts["count"],
    )
    fig.update_traces(textposition="outside")

    fig = apply_style_to_fig(fig)
    return fig


def graph_scatter_best_value(df: pd.DataFrame) -> go.Figure:
    """Create a scatter plot for best value."""
    if not len(df["Country"].unique()):
        raise ValueError("Please pass a DataFrame with only one country.")

    fig = px.scatter(
        df,
        x="Price",
        y="Award",
        size="Value",  # Larger bubbles indicate better value
        hover_name="Name",
        color="Value",
        labels={"Price": "Price Category", "Award": "Michelin Awards"},
        size_max=60,
        color_continuous_scale="Inferno",
        category_orders={"Award": list(reversed(MICHELIN_AWARDS_ORDERED))},
    )
    fig.update_xaxes(categoryorder="category ascending")
    fig = apply_style_to_fig(fig, apply_trace_color=False)
    return fig


def graph_heatmap_price(df: pd.DataFrame) -> go.Figure:
    """Create a heatmap using price and award."""
    if not len(df["Country"].unique()):
        raise ValueError("Please pass a DataFrame with only one country.")

    heatmap_data = pd.pivot_table(df, values="Name", index="Award", columns="Price", aggfunc="count")
    heatmap_data = heatmap_data.reindex(reversed(MICHELIN_AWARDS_ORDERED), level=0)

    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Price Category", y="Michelin Award", color="Count"),
        color_continuous_scale="Inferno",
    )
    fig = apply_style_to_fig(fig, apply_trace_color=False)
    return fig
