"""Shared database access for the data-analysis environment.

The PostgreSQL service runs as the `db` container of the devcontainer and is NOT
published to the host, so it is reachable ONLY from inside the devcontainer.
"""

from database.connection import check_connection, get_database_url, get_engine

__all__ = ["check_connection", "get_database_url", "get_engine"]
