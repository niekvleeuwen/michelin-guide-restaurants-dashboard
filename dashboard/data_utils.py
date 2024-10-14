import pandas as pd


def number_of_countries(df: pd.DataFrame) -> int:
    """Get the number of countries in the dataset."""
    return len(unique_countries(df))


def number_of_restaurants(df: pd.DataFrame) -> int:
    """Get the number of restaurants in the dataset."""
    return len(df["Name"].unique())


def top_cuisine(df: pd.DataFrame) -> int:
    """Get the top cuisine in the dataset."""
    data = df["Cuisine"].value_counts().index
    if len(data) == 0:
        return "-"
    return data[0]


def number_of_cities(df: pd.DataFrame) -> int:
    """Get the number of cities in the dataset."""
    return len(df[df["City"].notna()]["City"].unique())


def unique_countries(df: pd.DataFrame) -> pd.Series:
    """Get unique countries from the dataset."""
    return df[df["Country"].notna()]["Country"].unique()
