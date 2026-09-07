"""specs/feature-2-conversion.md: conversion rate by source. Red until you build it."""
import db
import logic
from conftest import use_temp_data


def expected_counts(source):
    """Count the leads and the won leads of one source straight from the table."""
    total = 0
    won = 0
    for lead in db.load_table("leads"):
        if lead["source"] == source:
            total = total + 1
            if lead["stage"] == "won":
                won = won + 1
    return total, won


def test_one_row_per_source_in_order(tmp_path, monkeypatch):
    """conversion_by_source returns one row per source, in the order of logic.SOURCES."""
    use_temp_data(tmp_path, monkeypatch)
    rows = logic.conversion_by_source()
    sources = []
    for row in rows:
        sources.append(row["source"])
    assert sources == logic.SOURCES


def test_totals_and_won_match_the_data(tmp_path, monkeypatch):
    """Each row's total and won numbers match the leads table."""
    use_temp_data(tmp_path, monkeypatch)
    for row in logic.conversion_by_source():
        total, won = expected_counts(row["source"])
        assert row["total"] == total
        assert row["won"] == won


def test_rate_is_a_percentage_with_one_decimal(tmp_path, monkeypatch):
    """rate is won divided by total, as a percentage rounded to one decimal."""
    use_temp_data(tmp_path, monkeypatch)
    for row in logic.conversion_by_source():
        assert row["rate"] == round(row["won"] / row["total"] * 100, 1)


def test_source_without_leads_has_rate_zero(tmp_path, monkeypatch):
    """A source with no leads shows 0 leads, 0 won and a rate of 0 instead of crashing."""
    use_temp_data(tmp_path, monkeypatch)
    remaining = []
    for lead in db.load_table("leads"):
        if lead["source"] != "event":
            remaining.append(lead)
    db.save_table("leads", remaining)

    for row in logic.conversion_by_source():
        if row["source"] == "event":
            assert row["total"] == 0
            assert row["won"] == 0
            assert row["rate"] == 0
