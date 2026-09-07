"""These tests should always pass. If one fails, something is wrong with your setup, not the code."""
import os

from streamlit.testing.v1 import AppTest

import db
import logic
import seed
from conftest import APP_FILE, REPO, TABLES, use_temp_data


def test_app_renders():
    """The home screen runs from top to bottom without raising an error."""
    app = AppTest.from_file(APP_FILE)
    app.run()
    assert not app.exception
    assert app.title[0].value == "Pipeline"


def test_tables_load():
    """The three CSV tables open, have the right columns, and hold a sensible number of leads."""
    for table in TABLES:
        rows = db.load_table(table)
        assert len(rows) > 0
        assert list(rows[0].keys()) == db.COLUMNS[table]
    assert 25 <= len(db.load_table("leads")) <= 35


def test_seed_restores_the_data(tmp_path, monkeypatch):
    """After changing the data, seed.reset puts every table back exactly as it was."""
    use_temp_data(tmp_path, monkeypatch)
    before = len(logic.all_leads())
    logic.add_lead("Someone", "Somewhere", "website", 100, "2026-12-01")
    assert len(logic.all_leads()) == before + 1

    seed.reset(str(tmp_path))

    for table in TABLES:
        with open(os.path.join(REPO, "seed", table + ".csv"), encoding="utf-8") as file:
            pristine = file.read()
        with open(os.path.join(tmp_path, table + ".csv"), encoding="utf-8") as file:
            restored = file.read()
        assert restored == pristine
