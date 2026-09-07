# Feature 2 — Conversion by source

## Why

As the owner, I want to know which channel brings leads that actually close, so that I spend the marketing budget on referrals, the website, LinkedIn or events based on numbers instead of gut feeling.

## What

- [ ] `logic.conversion_by_source()` returns a list with one dict per source, in the order of `logic.SOURCES`. Each dict has the keys `source`, `total`, `won` and `rate`.
- [ ] `total` is the number of leads with that source, `won` the number of those whose stage is `won`.
- [ ] `rate` is `won / total * 100`, rounded to one decimal.
- [ ] A source with no leads has `total` 0, `won` 0 and `rate` 0. The function does not crash on a division by zero.
- [ ] The Pipeline page has a section titled **Sources** showing the four rows (source, total, won, rate with a `%` sign).

## Out of scope

- Charts.
- Filtering by date range.
- Any source outside the four in `logic.SOURCES`.

## Done when

- `pytest tests/test_feature_2.py` is green, without changing the tests.
- The section shows up on the Pipeline page and the numbers match `data/leads.csv`.
- The work is on its own branch, with a commit message that says what you built.
