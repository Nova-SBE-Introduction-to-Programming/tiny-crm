# Feature 1 — Overdue follow-ups panel

> **Blocked by issue 002.** The panel is built on top of `overdue_followups`, which compares dates as text today. Fix that bug first (its test in `tests/test_bugs.py` must be green), otherwise the panel will show the wrong leads.

## Why

As a salesperson, I want to see at a glance which follow-ups I have missed and by how long, so that I chase the oldest ones first instead of scrolling through the whole pipeline.

## What

- [ ] `logic.days_overdue(followup_on, today)` returns the number of whole days between a stored follow-up date and `today`. It accepts dates with and without zero padding (`2026-9-5` and `2026-09-05` are the same day).
- [ ] `logic.overdue_report(today=None)` returns the overdue open leads, oldest first. Each item is the lead dict plus a `days_overdue` key with the number from `days_overdue`.
- [ ] Leads whose follow-up is today or later, and leads that are won or lost, are not in the report.
- [ ] The Pipeline page has a section titled **Overdue follow-ups** (a subheader with exactly that text) listing, for each item of the report, the name, company, follow-up date and the days overdue.

## Out of scope

- Sending reminders or emails.
- Changing the follow-up date from the panel.
- A per-stage breakdown of overdue leads.

## Done when

- `pytest tests/test_feature_1.py` is green, without changing the tests.
- The panel shows up on the Pipeline page and matches what you count by hand in `data/leads.csv`.
- The work is on its own branch, with a commit message that says what you built.
