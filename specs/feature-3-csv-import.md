# Feature 3 — Import leads from a CSV file

## Why

As a salesperson coming back from a trade fair with a spreadsheet of contacts, I want to upload it once instead of typing forty leads by hand, and I want to be told what was imported and what was ignored.

## What

- [ ] `logic.import_leads(csv_text)` takes the text of a CSV file with the columns `name,company,source,value` and appends the valid rows to `leads.csv`.
- [ ] Each imported lead has stage `new`, an empty `followup_on`, today's `created_on`, an empty `closed_on`, and a fresh id.
- [ ] A row is skipped when a lead with the same name and company already exists (duplicate).
- [ ] A row is skipped when the name is empty or the source is not one of `logic.SOURCES` (invalid).
- [ ] The function returns a dict `{"imported": n, "skipped": m}` with the two counts.
- [ ] Importing the same file twice imports nothing the second time; every row is skipped.
- [ ] A new **Import** screen in the sidebar uses `st.file_uploader` to pick the file, calls `import_leads`, and shows the summary ("Imported 2 leads, skipped 3").

## Out of scope

- Updating existing leads from the file.
- Importing notes or activities.
- Any column beyond the four above (extra columns are ignored, missing ones are an error you may show however you like).

## Done when

- `pytest tests/test_feature_3.py` is green, without changing the tests.
- Uploading a small CSV in the UI adds the rows to `data/leads.csv` and shows the summary.
- The work is on its own branch, with a commit message that says what you built.
