from pathlib import Path
import pandas as pd
import urllib.request
from loguru import logger

URL = "https://raw.githubusercontent.com/plotly/datasets/master/michelin_by_Jerry_Ng.csv"
CACHE_FILE = "data/michelin_data.csv"


def load_data() -> pd.DataFrame:
    """Load data.

    The data is either retrieved from cache, or fetched from Github if not found in cache.

    Returns:
        pd.DataFrame: CSV data as a pandas DataFrame
    """
    path = Path(CACHE_FILE)

    if not path.is_file():
        fetch_data(path)
    else:
        logger.info("Loading data from cache..")

    df = pd.read_csv(path)

    df = clean_data(df)

    df = add_features(df)

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
    # Convert comma delimited string to array
    df["FacilitiesAndServices"] = df["FacilitiesAndServices"].str.split(",")

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
