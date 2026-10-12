"""Auth schema upkeep for databases created before newer columns existed.

Account approval (``users.is_approved``) is the only access gate besides the
password: new signups stay locked until the super admin accepts them. The
retired email-verification flow's ``email_otps`` table is dropped when found.
"""
from __future__ import annotations

from sqlalchemy.engine import Engine


def ensure_user_columns(engine: Engine) -> int:
    """Add ``users.is_verified`` / ``users.is_approved`` to databases created
    before these features, grandfathering pre-existing accounts instead of
    locking them out. Drops the retired ``email_otps`` table. Returns rows
    backfilled.
    """
    from sqlalchemy import inspect, text

    columns = {column["name"] for column in inspect(engine).get_columns("users")}
    backfilled = 0
    with engine.begin() as connection:
        for column in ("is_verified", "is_approved"):
            if column not in columns:
                connection.execute(
                    text(f"ALTER TABLE users ADD COLUMN {column} BOOLEAN DEFAULT FALSE")
                )
                # The column is brand new, so every row predates the feature.
                backfilled += connection.execute(
                    text(f"UPDATE users SET {column} = TRUE")
                ).rowcount or 0
        if not backfilled:
            for column in ("is_verified", "is_approved"):
                backfilled += connection.execute(
                    text(f"UPDATE users SET {column} = TRUE WHERE {column} IS NULL")
                ).rowcount or 0
        connection.execute(text("DROP TABLE IF EXISTS email_otps"))
    return backfilled
