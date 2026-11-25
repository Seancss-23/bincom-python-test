# Bincom Python Trainee Test

Solutions to the Bincom Dev Center Python test, by Sean Okpara. The program reads `python_class_question.html` (the colours staff wore for a week) and answers every question, including the bonuses and the 1s puzzle.

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python main.py                  # full report, asks for one number for Q7
python -m pytest                # tests
```

### PostgreSQL (Q6)

I used a free Supabase Postgres database.

1. Supabase dashboard, open your project, click **Connect**, choose **Session pooler**, copy the URI.
2. Copy `.env.example` to `.env` and set `DATABASE_URL` to that URI, with your real password in place of `[YOUR-PASSWORD]`.
3. Run `python main.py`.

`.env` is git-ignored. If `DATABASE_URL` is missing or the database can't be reached, Q6 prints a "Skipped" message and the rest of the report still runs.

The table is `colour_frequencies (colour TEXT PRIMARY KEY, frequency INTEGER NOT NULL CHECK (frequency >= 0))`. It is created if missing, filled with an upsert (`INSERT ... ON CONFLICT DO UPDATE`, so re-running just updates the counts), then read back and printed. All values go through parameterised queries. Row Level Security is switched on for the table, since Supabase exposes public tables through its API; this program connects as the owner role, which bypasses RLS.

## Files

| File | What it does |
|---|---|
| `main.py` | Runs Q1 to Q9 and the puzzle, prints a labelled report |
| `colours.py` | Reads the HTML and works out the statistics (Q1-Q5) |
| `db.py` | Saves and reads back the frequencies in PostgreSQL (Q6) |
| `algorithms.py` | Recursive search, base-10, Fibonacci, 1s puzzle (Q7-Q9) |
| `tests/test_solution.py` | pytest checks for all of the above |

## Answers

The table holds 95 colour values (19 a day for 5 days) across 11 distinct colours.

| Colour | Count | | Colour | Count |
|---|---|---|---|---|
| BLUE | 31 | | BROWN | 6 |
| WHITE | 16 | | YELLOW | 5 |
| GREEN | 10 | | PINK | 5 |
| ORANGE | 9 | | CREAM | 2 |
| RED | 9 | | ARSH | 1 |
| | | | BLACK | 1 |

| Question | Answer |
|---|---|
| 1. Mean colour | ORANGE and RED (tie) |
| 2. Most worn colour | BLUE (31 of 95) |
| 3. Median colour | GREEN |
| 4. Variance (bonus) | 68.23 population (75.05 sample) |
| 5. P(red) (bonus) | 9/95 = 0.0947 = 9.47% |
| 6. PostgreSQL | Table `colour_frequencies`, see above |
| 7. Recursive search (bonus) | Recursive binary search, returns the index or "not found" |
| 8. Random binary to base 10 | Different every run, e.g. `1011` = 11 |
| 9. Sum of first 50 Fibonacci | 20365011073 |
| Puzzle | `0000000000100000000100000000001` (matches the sample) |

## Assumptions

- **Parsing:** the colours are read from the HTML with a regex, nothing is hard-coded. Every value is stripped and upper-cased.
- **Mean colour:** colours aren't numbers, so I take the mean frequency (95 / 11 = 8.64) and return the colour(s) whose count is closest. ORANGE and RED tie at 9, so both are reported.
- **Mode:** the colour with the highest count.
- **Median colour:** all 95 values sorted A-Z, then the middle one (the 48th, index 47).
- **Variance:** of the colour frequencies. I use the population formula (divide by n) because the data is the full week, not a sample. The sample figure (divide by n-1) is printed too.
- **P(red):** red count divided by all 95 values.
- **Recursive search:** binary search, so the list must be sorted (the program sorts it first). Input is validated; non-numbers are asked again.
- **Fibonacci:** starts 0, 1, 1, 2, ... and is summed with a loop. If it started 1, 1, 2, the answer would be the same, because the leading 0 adds nothing.
- **Base 10:** `random.choice` is used four times to build the bits. They are converted with my own loop (powers of 2) and checked against `int(bits, 2)`.
- **Puzzle:** the output has a 1 at the end of each run of exactly three 1s. Runs of 1, 2, 4 or more give only 0s.

## Data quirks

- `BLEW` (Tuesday) is treated as a typo of `BLUE` and counted as BLUE. Without that fix BLUE would be 30.
- `ARSH` (Tuesday) is left as it is. It could be "ASH", but that is a guess, so it stays its own colour with a count of 1.
