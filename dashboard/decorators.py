import pandas as pd


def filter_by_country(func):
    def wrapper(df, country, *args, **kwargs):
        # Convert the dictionary to DataFrame and filter by country
        filtered_df = df[df["Country"] == country]

        # Call the original function with the filtered DataFrame
        return func(filtered_df, *args, **kwargs)

    return wrapper


def df_from_dict(func):
    def wrapper(df_dict, *args, **kwargs):
        # Convert the dictionary to DataFrame
        df = pd.DataFrame.from_dict(df_dict)

        # Call the original function with the filtered DataFrame
        return func(df, *args, **kwargs)

    return wrapper
