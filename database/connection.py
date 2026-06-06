"""Structured PostgreSQL connection for the data-analysis environment.

The database runs as the `db` container of the devcontainer and is NOT published to
the host (see .devcontainer/docker-compose.yml), so it is only reachable from inside
the devcontainer. Connection settings come from the DATABASE_URL environment variable
(set on the `app` service in the compose file), with a default that matches it.

Typical usage from a chapter, with pandas:

    import pandas as pd
    from database import get_engine

    df = pd.read_sql("SELECT * FROM my_table", get_engine())
    df.to_sql("my_table", get_engine(), if_exists="replace", index=False)
"""

from __future__ import annotations

import os
from functools import lru_cache

from sqlalchemy import Engine, create_engine, text

# Matches the credentials and host in .devcontainer/docker-compose.yml. The host is
# "localhost" because the app container shares the db container's network namespace
# (network_mode: service:db).
DEFAULT_DATABASE_URL = (
    "postgresql+psycopg2://sparrow:1009@localhost:5432/data_analysis_db"
)


def get_database_url() -> str:
    """Return DATABASE_URL from the environment, or the devcontainer default."""
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Create (once) and return a SQLAlchemy engine for the project database.

    The engine is cached so the whole project shares a single connection pool.
    """
    return create_engine(get_database_url(), future=True)


def check_connection() -> str:
    """Open a connection and return the PostgreSQL server version (a smoke test)."""
    with get_engine().connect() as connection:
        version: str = connection.execute(text("SELECT version()")).scalar_one()
        return version


if __name__ == "__main__":
    print("Connecting to:", get_database_url())
    print(check_connection())
