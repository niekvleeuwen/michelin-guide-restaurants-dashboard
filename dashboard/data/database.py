from pathlib import Path

import pandas as pd
from langchain_community.utilities import SQLDatabase
from loguru import logger
from sqlalchemy import create_engine

from dashboard.singleton import SingletonMeta


class Database(metaclass=SingletonMeta):
    """Provide CSV data as a SQLite database."""

    DB_FILE = Path("cache/michelin.db")

    def __init__(self):
        logger.debug("Database object is being created..")
        self.db = None

    def load(self, df: pd.DataFrame) -> None:
        database_exists = self.DB_FILE.is_file()

        engine = create_engine(f"sqlite:///{self.DB_FILE}")

        # Load data into database if the database did not exists
        if not database_exists:
            df.to_sql("michelin", engine, index=False)

        self.db = SQLDatabase(engine=engine)

    def get_db(self) -> SQLDatabase:
        """Return instance of SQLDatabase."""
        if not self.db:
            raise AttributeError("Database has not been initialized yet.")
        return self.db
