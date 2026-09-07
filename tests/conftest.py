"""Shared test setup. pytest loads this file automatically before the tests."""
import os
import shutil
import sys

# The tests live in tests/ and the app one folder up, so make the app importable.
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import db

APP_FILE = os.path.join(REPO, "app.py")
TABLES = ["leads", "notes", "activities"]


def use_temp_data(tmp_path, monkeypatch):
    """Copy seed/*.csv into a throwaway folder and point db at it, so data/ is never touched."""
    for table in TABLES:
        source = os.path.join(REPO, "seed", table + ".csv")
        shutil.copyfile(source, os.path.join(tmp_path, table + ".csv"))
    monkeypatch.setattr(db, "DATA_DIR", str(tmp_path))


def ids_of(leads):
    """Return just the ids of a list of leads, to make comparisons short."""
    ids = []
    for lead in leads:
        ids.append(lead["id"])
    return ids


def make_lead(lead_id, followup_on, stage="contacted"):
    """Build a complete lead dict for a test, with only the fields that matter passed in."""
    return {
        "id": lead_id,
        "name": "Lead " + lead_id,
        "company": "Company " + lead_id,
        "source": "website",
        "stage": stage,
        "value": "1000",
        "followup_on": followup_on,
        "created_on": "2026-06-01",
        "closed_on": "",
    }
