"""One test per issue in issues/. Each test describes the CORRECT behaviour, so it is red until you fix the bug."""
from datetime import date

import db
import logic
from conftest import ids_of, make_lead, use_temp_data


def test_000_count_by_stage_matches_the_data(tmp_path, monkeypatch):
    """issues/000: the per-stage count equals the number of leads really in that stage."""
    use_temp_data(tmp_path, monkeypatch)
    for stage in logic.STAGES:
        expected = 0
        for lead in db.load_table("leads"):
            if lead["stage"] == stage:
                expected = expected + 1
        assert logic.count_by_stage(stage) == expected


def test_001_search_ignores_case(tmp_path, monkeypatch):
    """issues/001: 'acme' and 'ACME' find the same leads as 'Acme'."""
    use_temp_data(tmp_path, monkeypatch)
    with_capital = ids_of(logic.search_leads("Acme"))
    assert len(with_capital) >= 1
    assert ids_of(logic.search_leads("acme")) == with_capital
    assert ids_of(logic.search_leads("ACME")) == with_capital


def test_002_overdue_compares_real_dates(tmp_path, monkeypatch):
    """issues/002: overdue leads are found and ordered by date, padded or not."""
    use_temp_data(tmp_path, monkeypatch)
    today = date(2026, 10, 1)
    db.save_table("leads", [
        make_lead("1", "2026-8-28"),
        make_lead("2", "2026-9-5"),
        make_lead("3", "2026-09-20"),
        make_lead("4", "2026-10-15"),
        make_lead("5", "2026-10-01"),
        make_lead("6", "2026-7-1", stage="lost"),
    ])
    assert ids_of(logic.overdue_followups(today)) == ["1", "2", "3"]


def test_003_mark_won_stamps_closed_on_and_counts(tmp_path, monkeypatch):
    """issues/003: winning a lead records today as closed_on, and 'won this month' counts it."""
    use_temp_data(tmp_path, monkeypatch)
    lead = logic.leads_in_stage("proposal")[0]

    logic.mark_won(lead["id"])

    updated = logic.get_lead(lead["id"])
    assert updated["stage"] == "won"
    assert updated["closed_on"] == str(date.today())
    assert logic.won_this_month() == 1
