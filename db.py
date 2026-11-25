"""Save the colour frequencies in PostgreSQL and read them back (Q6)."""

import os

import psycopg
from dotenv import load_dotenv

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS colour_frequencies (
    colour    TEXT PRIMARY KEY,
    frequency INTEGER NOT NULL CHECK (frequency >= 0)
)
"""

# Supabase exposes public tables through its API, so switch RLS on. With no
# policies that means the API can't touch the table; this script connects as
# the owner role, which bypasses RLS, so it still works.
ENABLE_RLS = "ALTER TABLE colour_frequencies ENABLE ROW LEVEL SECURITY"

# Upsert: re-running the program updates the counts instead of failing on
# the primary key. Values are passed separately, never pasted into the text.
UPSERT = """
INSERT INTO colour_frequencies (colour, frequency) VALUES (%s, %s)
ON CONFLICT (colour) DO UPDATE SET frequency = EXCLUDED.frequency
"""

SELECT_ALL = "SELECT colour, frequency FROM colour_frequencies ORDER BY frequency DESC, colour"


def save_and_read_back(counts):
    """Upsert the counts, then return the rows stored in the database.

    Returns None (with a message) when DATABASE_URL is missing or the
    database can't be reached, so the rest of the report still runs.
    """
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        print("    Skipped: DATABASE_URL is not set. Copy .env.example to .env and add it.")
        return None
    try:
        with psycopg.connect(url) as conn:
            conn.execute(CREATE_TABLE)
            conn.execute(ENABLE_RLS)
            conn.cursor().executemany(UPSERT, list(counts.items()))
            return conn.execute(SELECT_ALL).fetchall()
    except psycopg.Error as error:
        # Print only the error class: the message can echo connection details.
        print(f"    Skipped: could not use the database ({type(error).__name__}).")
        return None
