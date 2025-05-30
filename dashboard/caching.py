import pandas as pd
from flask_caching import Cache

from dashboard.data.loader import load_data

TIMEOUT = 60 * 60 * 24  # Cache data for approximately 1 day

cache = Cache(config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache"})


@cache.memoize(timeout=TIMEOUT)
def retrieve_data() -> pd.DataFrame:
    """Function used to cache data."""
    data = load_data()
    return data
