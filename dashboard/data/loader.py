import urllib.request
from pathlib import Path

import pandas as pd
from loguru import logger

from dashboard.data.database import Database

URL = "https://raw.githubusercontent.com/plotly/datasets/master/michelin_by_Jerry_Ng.csv"
CACHE_FILE = "cache/michelin_data.csv"


def load_data() -> pd.DataFrame:
    """Load data.

    The data is either retrieved from cache, or fetched from Github if not found in cache.

    Returns:
        pd.DataFrame: CSV data as a pandas DataFrame
    """
    path = Path(CACHE_FILE)

    if not path.is_file():
        logger.info("Fetching data from source..")
        fetch_data(path)
    else:
        logger.info("Loading data from cache..")

    df = pd.read_csv(path)

    df = clean_data(df)

    df = add_features(df)

    logger.info("Loading data into SQLite database..")
    Database().load(df)

    return df


def fetch_data(path: Path) -> None:
    """Fetches data from URL and stores the data in the cache file.

    Args:
        cache_path (Path): path to store the fetched data
    """
    logger.info("Fetching data..")
    path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(URL, path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataset."""

    # Correct column to a boolean type
    df["GreenStar"] = df["GreenStar"].astype(bool)

    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add features to the dataframe.

    Args:
        df (pd.DataFrame): original dataframe as retrieved from Github

    Returns:
        pd.DataFrame: dataset with features
    """
    df = add_award_size_feature(df)
    df = add_city_country_features(df)
    df = normalize_price(df)
    df = add_value_feature(df)
    return df


def add_award_size_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Add a size based to be used for maps based on the value of 'Award'."""

    def size_mapping(award):
        if award == "3 Stars":
            return 30
        elif award == "2 Stars":
            return 15
        elif award == "1 Star":
            return 10
        elif award == "Bib Gourmand":
            return 5
        else:
            return 2

    df["Award (Map Size)"] = df["Award"].apply(size_mapping)
    return df


def add_city_country_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add 'City' and 'Country' features based on the column 'Location'."""

    df[["City", "Country"]] = df["Location"].str.split(", ", n=1, expand=True)

    # Correct for locations with the same value for City and Country (e.g. Singapore)
    df.loc[df["Country"].isnull(), "Country"] = df["Location"]

    return df


def normalize_price(df: pd.DataFrame) -> pd.DataFrame:
    """Add column 'Price (normalized)'.

    Based on the length of the string.
    """

    def price_mapping(price):
        if pd.isna(price):
            return price

        length = len(price)

        if length == 1:
            return "Budget-Friendly"
        elif length == 2:
            return "Moderate"
        elif length == 3:
            return "Premium"
        elif length == 4:
            return "Luxury"
        raise ValueError("Unknown price")

    df["Price (normalized)"] = df["Price"].apply(price_mapping)
    return df


def add_value_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Add 'value feature'. Based on the 'price' and 'award' column.

    Higher Award at Lower Price = Better Value

    Args:
        df (pd.DataFrame): dataframe (including column 'Price (normalized)' and 'Award')

    Returns:
        pd.DataFrame: dataframe with added feature.
    """
    price_mapping = {"Budget-Friendly": 1, "Moderate": 2, "Premium": 3, "Luxury": 4}
    award_mapping = {"Selected Restaurants": 1, "Bib Gourmand": 2, "1 Star": 3, "2 Stars": 4, "3 Stars": 5}

    df["Price Score"] = df["Price (normalized)"].map(price_mapping)
    df["Award Score"] = df["Award"].map(award_mapping)

    # Create a 'Value' column: Higher Award at Lower Price = Better Value
    df["Value"] = (df["Award Score"] / df["Price Score"]).round(1)

    return df
