"""specs/feature-3-csv-import.md: import leads from a CSV file. Red until you build it."""
import logic
from conftest import use_temp_data

# Four rows: one new, one duplicate of a seed lead, one without a name, one with an unknown source.
CSV_TEXT = (
    "name,company,source,value\n"
    "Teresa Lima,Sapataria Lima,website,500\n"
    "Ana Ferreira,Padaria Central,referral,1200\n"
    ",Empresa Sem Nome,event,100\n"
    "Jorge Cunha,Cunha & Irmaos,tiktok,300\n"
    "Paulo Melo,Melo Seguros,linkedin,900\n"
)


def find_lead(name, company):
    """Return every lead with this exact name and company."""
    found = []
    for lead in logic.all_leads():
        if lead["name"] == name and lead["company"] == company:
            found.append(lead)
    return found


def test_valid_rows_become_new_leads(tmp_path, monkeypatch):
    """Each valid row is appended as a lead in stage 'new' with an empty follow-up date."""
    use_temp_data(tmp_path, monkeypatch)
    before = len(logic.all_leads())
    logic.import_leads(CSV_TEXT)
    assert len(logic.all_leads()) == before + 2

    teresa = find_lead("Teresa Lima", "Sapataria Lima")[0]
    assert teresa["stage"] == "new"
    assert teresa["source"] == "website"
    assert teresa["value"] == "500"
    assert teresa["followup_on"] == ""
    assert teresa["closed_on"] == ""


def test_duplicates_are_skipped(tmp_path, monkeypatch):
    """A row with the same name and company as an existing lead is not added again."""
    use_temp_data(tmp_path, monkeypatch)
    logic.import_leads(CSV_TEXT)
    assert len(find_lead("Ana Ferreira", "Padaria Central")) == 1


def test_invalid_rows_are_skipped(tmp_path, monkeypatch):
    """Rows without a name, or with a source that is not in logic.SOURCES, are not added."""
    use_temp_data(tmp_path, monkeypatch)
    logic.import_leads(CSV_TEXT)
    assert find_lead("", "Empresa Sem Nome") == []
    assert find_lead("Jorge Cunha", "Cunha & Irmaos") == []


def test_summary_counts_imported_and_skipped(tmp_path, monkeypatch):
    """import_leads returns how many rows were imported and how many were skipped."""
    use_temp_data(tmp_path, monkeypatch)
    summary = logic.import_leads(CSV_TEXT)
    assert summary == {"imported": 2, "skipped": 3}


def test_importing_the_same_file_twice_adds_nothing(tmp_path, monkeypatch):
    """Running the same import again skips every row."""
    use_temp_data(tmp_path, monkeypatch)
    logic.import_leads(CSV_TEXT)
    again = logic.import_leads(CSV_TEXT)
    assert again == {"imported": 0, "skipped": 5}
    assert len(find_lead("Teresa Lima", "Sapataria Lima")) == 1
