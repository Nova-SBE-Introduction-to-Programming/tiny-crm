"""Tiny CRM: every screen of the app lives here. Start it with `streamlit run app.py`."""
import streamlit as st

import logic

SCREENS = ["Pipeline", "Lead", "Add lead"]


# ---------- small helpers ----------

def lead_label(lead_id):
    """Turn a lead id into the text shown in the lead picker, e.g. 'Ana — Padaria Central'."""
    lead = logic.get_lead(lead_id)
    return lead["name"] + " — " + lead["company"]


def ids_of(leads):
    """Return just the ids of a list of leads."""
    ids = []
    for lead in leads:
        ids.append(lead["id"])
    return ids


def lead_line(lead, overdue_ids):
    """Build the one-line summary of a lead used in the pipeline lists."""
    text = "**" + lead["name"] + "** · " + lead["company"] + " · " + lead["value"] + " €"
    text = text + " · follow-up " + lead["followup_on"]
    if lead["id"] in overdue_ids:
        text = text + " · :red[overdue]"
    return text


# ---------- screen 1: pipeline ----------

def show_pipeline():
    """Home screen: one number per stage, a search box, and the leads grouped by stage."""
    st.title("Pipeline")

    columns = st.columns(len(logic.STAGES))
    for position in range(len(logic.STAGES)):
        stage = logic.STAGES[position]
        columns[position].metric(stage, logic.count_by_stage(stage))

    overdue_ids = ids_of(logic.overdue_followups())
    left, right = st.columns(2)
    left.metric("Won this month", logic.won_this_month())
    right.metric("Overdue follow-ups", len(overdue_ids))

    query = st.text_input("Search by name or company")
    leads = logic.search_leads(query)

    for stage in logic.STAGES:
        st.subheader(stage)
        for lead in leads:
            if lead["stage"] == stage:
                st.markdown(lead_line(lead, overdue_ids))


# ---------- screen 2: lead page ----------

def show_lead():
    """Lead screen: every field, the stage buttons, the notes thread and the activities."""
    st.title("Lead")
    leads = logic.all_leads()
    if len(leads) == 0:
        st.info("No leads yet. Add one first.")
        return

    lead_id = st.selectbox("Pick a lead", ids_of(leads), format_func=lead_label)
    lead = logic.get_lead(lead_id)

    show_fields(lead)
    show_stage_buttons(lead)
    show_notes(lead_id)
    show_activities(lead_id)

    st.divider()
    if st.button("Delete lead"):
        logic.delete_lead(lead_id)
        st.rerun()


def show_fields(lead):
    """Print every field of a lead in two columns."""
    overdue_ids = ids_of(logic.overdue_followups())
    followup = lead["followup_on"]
    if lead["id"] in overdue_ids:
        followup = followup + " :red[(overdue)]"

    left, right = st.columns(2)
    left.markdown("**Name:** " + lead["name"])
    left.markdown("**Company:** " + lead["company"])
    left.markdown("**Source:** " + lead["source"])
    left.markdown("**Value:** " + lead["value"] + " €")
    right.markdown("**Stage:** " + lead["stage"])
    right.markdown("**Follow-up on:** " + followup)
    right.markdown("**Created on:** " + lead["created_on"])
    right.markdown("**Closed on:** " + lead["closed_on"])


def show_stage_buttons(lead):
    """Show the buttons that move a lead along the pipeline."""
    if lead["stage"] == "won" or lead["stage"] == "lost":
        st.caption("This deal is closed.")
        return

    col1, col2, col3 = st.columns(3)
    following = logic.next_stage(lead["stage"])
    if following is not None:
        if col1.button("Move to next stage (" + following + ")"):
            logic.move_to_next_stage(lead["id"])
            st.rerun()
    if col2.button("Mark won"):
        logic.mark_won(lead["id"])
        st.rerun()
    if col3.button("Mark lost"):
        logic.move_to_stage(lead["id"], "lost")
        st.info("Coming soon")


def show_notes(lead_id):
    """Show the notes thread of a lead and the form to add a new note."""
    st.subheader("Notes")
    notes = logic.notes_for(lead_id)
    if len(notes) == 0:
        st.caption("No notes yet.")
    for note in notes:
        st.markdown("**" + note["created_on"] + "** — " + note["text"])

    with st.form("add_note", clear_on_submit=True):
        text = st.text_area("New note")
        if st.form_submit_button("Add note"):
            logic.add_note(lead_id, text)
            st.rerun()


def show_activities(lead_id):
    """List what happened with this lead: calls, emails, meetings, stage moves."""
    st.subheader("Activity")
    activities = logic.activities_for(lead_id)
    if len(activities) == 0:
        st.caption("Nothing recorded yet.")
    for activity in activities:
        st.markdown(activity["created_on"] + " — " + activity["kind"])


# ---------- screen 3: add lead ----------

def show_add_lead():
    """Form to create a new lead. It goes straight into the 'new' stage."""
    st.title("Add lead")
    with st.form("add_lead", clear_on_submit=True):
        name = st.text_input("Name")
        company = st.text_input("Company")
        source = st.selectbox("Source", logic.SOURCES)
        value = st.number_input("Value (€)", min_value=0, step=100)
        followup_on = st.date_input("Follow-up on")
        if st.form_submit_button("Save lead"):
            new_id = logic.add_lead(name, company, source, value, str(followup_on))
            st.success("Saved lead #" + str(new_id) + ". Open data/leads.csv to see the new row.")


# ---------- this part runs on every click ----------

st.set_page_config(page_title="Tiny CRM")
st.sidebar.title("Tiny CRM")
screen = st.sidebar.radio("Screen", SCREENS)
st.sidebar.caption("The data lives in data/*.csv. Reset it with `python seed.py`.")

if screen == "Pipeline":
    show_pipeline()
elif screen == "Lead":
    show_lead()
else:
    show_add_lead()
