"""Schema upkeep for My Jobs List on databases created before newer columns.

Follows the same pattern as ``email_otp.ensure_user_columns``: plain
``ALTER TABLE`` guarded by inspection, so Render reboots and local SQLite
both migrate without an alembic revision.
"""
from __future__ import annotations

from sqlalchemy.engine import Engine


def ensure_myjob_columns(engine: Engine) -> int:
    """Add ``my_jobs.resources`` (free YouTube/practice links) when missing.

    Returns the number of rows backfilled.
    """
    from sqlalchemy import inspect, text

    if "my_jobs" not in inspect(engine).get_table_names():
        return 0
    columns = {column["name"] for column in inspect(engine).get_columns("my_jobs")}
    if "resources" in columns:
        return 0
    dialect = engine.dialect.name
    default = "'[]'::json" if dialect == "postgresql" else "'[]'"
    backfilled = 0
    with engine.begin() as connection:
        connection.execute(text(f"ALTER TABLE my_jobs ADD COLUMN resources JSON DEFAULT {default}"))
        backfilled = connection.execute(
            text("UPDATE my_jobs SET resources = '[]' WHERE resources IS NULL")
        ).rowcount or 0
    return backfilled
