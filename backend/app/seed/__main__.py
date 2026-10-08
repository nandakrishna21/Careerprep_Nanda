"""Run the seeder: `python -m app.seed` (safe to run repeatedly)."""
from __future__ import annotations

from app.core.database import Base, SessionLocal, engine
from app.seed import run
from app.services.job_taxonomy import backfill_jobs


def main() -> None:
    Base.metadata.create_all(engine)
    backfill_jobs(engine)
    db = SessionLocal()
    try:
        added = run(db)
    finally:
        db.close()
    print("Seed complete (rows added):")
    for name, value in added.items():
        print(f"  {name:18} +{value}")


if __name__ == "__main__":
    main()
