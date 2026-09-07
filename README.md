# Tiny CRM

Tiny CRM is a minimal sales pipeline for a small company: leads move through the stages `new → contacted → proposal → won / lost`, and each lead carries notes, activities and a follow-up date. It is also the codebase you will read, question, fix and extend during this course.

## Run it

Unzip the project, open the folder in your editor, open a terminal inside it, then:

```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Reset the data

The app writes to the CSV files in `data/`. When you want the original data back:

```
python seed.py
```

## Run the tests

```
pytest
```

Some tests fail on purpose. They describe features not built yet and bugs not fixed yet. That's your job.

## Folder map

```
app.py               all the Streamlit screens (start here)
db.py                reads and writes the CSV files: load_table, save_table, append_row, next_id
logic.py             the business rules: stages, search, overdue follow-ups, home-page numbers
seed.py              python seed.py -> resets data/ from seed/
data/leads.csv       the live "database", one file per table
data/notes.csv
data/activities.csv
seed/                pristine copies of the three CSV files
tests/test_smoke.py  always green: the app imports, the tables load, seed works
tests/test_bugs.py   red until you fix the bugs described in issues/
tests/test_feature_1.py  red until you build specs/feature-1-overdue.md
tests/test_feature_2.py  red until you build specs/feature-2-conversion.md
tests/test_feature_3.py  red until you build specs/feature-3-csv-import.md
tests/conftest.py    shared test helpers (a throwaway copy of the data for each test)
specs/               what to build, written by a product manager
issues/              what is broken, written by a user
ONBOARDING.md        the week-1 question sheet: answer it in this file
requirements.txt     streamlit and pytest, pinned
```
