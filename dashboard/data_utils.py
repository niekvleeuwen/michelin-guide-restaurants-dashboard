import pandas as pd


def number_of_countries(df: pd.DataFrame) -> int:
    """Get the number of countries in the dataset."""
    return len(df[df["Country"].notna()]["Country"].unique())


def number_of_restaurants(df: pd.DataFrame) -> int:
    """Get the number of restaurants in the dataset."""
    return len(df["Name"].unique())


def top_cuisine(df: pd.DataFrame) -> int:
    """Get the top cuisine in the dataset."""
    return df["Cuisine"].value_counts().index[0]


def number_of_cities(df: pd.DataFrame) -> int:
    """Get the number of cities in the dataset."""
    return len(df[df["City"].notna()]["City"].unique())
