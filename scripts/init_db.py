"""Create an empty database from a schema, without overwriting existing files."""
import argparse
import sqlite3
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--love", action="store_true", help="Initialize the separate experimental bot database")
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
schema = root / "schema" / ("love.sql" if args.love else "schedule.sql")
target = root / "config" / ("db_love.db" if args.love else "database.db")
with target.open("xb"):
    pass
try:
    with sqlite3.connect(target) as connection:
        connection.executescript(schema.read_text())
except Exception:
    target.unlink()
    raise
print(f"Created empty database: {target.name}")
