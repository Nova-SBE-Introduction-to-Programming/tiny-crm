"""specs/feature-1-overdue.md: the 'Overdue follow-ups' panel. Red until you build it (blocked by issue 002)."""
from datetime import date

from streamlit.testing.v1 import AppTest

import db
import logic
from conftest import APP_FILE, ids_of, make_lead, use_temp_data


def save_mixed_fixture():
    """Write six leads with padded and unpadded dates around 1 October 2026."""
    db.save_table("leads", [
        make_lead("1", "2026-8-28"),
        make_lead("2", "2026-9-5"),
        make_lead("3", "2026-09-20"),
        make_lead("4", "2026-10-15"),
        make_lead("5", "2026-10-01"),
        make_lead("6", "2026-7-1", stage="lost"),
    ])


def test_days_overdue_counts_whole_days():
    """days_overdue turns a stored date (padded or not) and today into a number of days."""
    assert logic.days_overdue("2026-9-5", date(2026, 10, 1)) == 26
    assert logic.days_overdue("2026-09-30", date(2026, 10, 1)) == 1


def test_overdue_report_is_oldest_first_with_days(tmp_path, monkeypatch):
    """overdue_report returns the overdue leads, oldest first, each with a days_overdue number."""
    use_temp_data(tmp_path, monkeypatch)
    save_mixed_fixture()
    report = logic.overdue_report(date(2026, 10, 1))
    assert ids_of(report) == ["1", "2", "3"]
    days = []
    for row in report:
        days.append(row["days_overdue"])
    assert days == [34, 26, 11]


def test_overdue_report_skips_future_and_closed_leads(tmp_path, monkeypatch):
    """Leads due today or later, and won or lost leads, are not in the report."""
    use_temp_data(tmp_path, monkeypatch)
    save_mixed_fixture()
    report_ids = ids_of(logic.overdue_report(date(2026, 10, 1)))
    assert "4" not in report_ids
    assert "5" not in report_ids
    assert "6" not in report_ids


def test_home_page_has_an_overdue_panel(tmp_path, monkeypatch):
    """The home screen shows a section titled 'Overdue follow-ups'."""
    use_temp_data(tmp_path, monkeypatch)
    app = AppTest.from_file(APP_FILE)
    app.run()
    assert not app.exception
    titles = []
    for header in app.subheader:
        titles.append(header.value)
    assert "Overdue follow-ups" in titles
