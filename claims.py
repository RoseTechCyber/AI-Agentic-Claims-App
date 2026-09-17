import streamlit as st
import sqlite3
import pandas as pd

from ClaimsAgents.triage_agent import assess_claim
from ClaimsAgents.supplier_agent import recommend_supplier

DB_NAME = "database/claims.db"


def save_note(conn, claim_id, note_text):
    conn.execute("""
        INSERT INTO ClaimNotes (
            ClaimID,
            NoteDate,
            NoteType,
            NoteText,
            CreatedBy,
            CreatedByRole,
            Visibility,
            IsFraudRelated
        )
        VALUES (
            ?, datetime('now'),
            'Assessment',
            ?,
            'System',
            'ClaimsAgent',
            'Internal',
            0
        )
    """, (claim_id, note_text))


def create_action(conn, claim_id, action_text):
    conn.execute("""
        INSERT INTO ClaimActions (
            ClaimID,
            ActionDate,
            ActionType,
            ActionDescription,
            Status,
            CreatedBy
        )
        VALUES (
            ?,
            datetime('now'),
            'Follow Up',
            ?,
            'Open',
            'ClaimsAgent'
        )
    """, (claim_id, action_text))


def assign_supplier(conn, claim_id, supplier):
    conn.execute("""
        INSERT INTO ClaimAssignments (
            ClaimID,
            AssignmentType,
            AssignedEntity,
            AssignedDate,
            AssignmentStatus,
            Reason,
            AssignedBy
        )
        VALUES (
            ?,
            'Supplier',
            ?,
            datetime('now'),
            'Active',
            'AI Recommendation',
            'SupplierAgent'
        )
    """, (claim_id, supplier))

from database.db_utils import (get_all_claims, get_claim_context)
def get_playbook_actions(
    conn,
    claim_type,
    priority,
    fraud_risk
):

    return pd.read_sql_query(
        """
        SELECT *
        FROM Claims_Playbooks
        WHERE ClaimType = ?
        AND Priority = ?
        AND FraudRisk = ?
        AND Active = 'Yes'
        """,
        conn,
        params=(
            claim_type,
            priority,
            fraud_risk
        )
    )

def process_claim(claim):

    context = get_claim_context(
        claim["ClaimID"]
    )

    conn = sqlite3.connect(DB_NAME)

    triage = assess_claim(
        claim,
        context["notes"]
    )

    playbooks = get_playbook_actions(
        conn,
        claim["ClaimType"],
        triage["priority"],
        triage["fraud_risk"]
    )    
    if playbooks.empty:

        save_note(
        conn,
        claim["ClaimID"],
        "No matching Claims Playbook found"
       )   

    save_note(
        conn,
        claim["ClaimID"],
        f"Priority={triage['priority']}, "
        f"Fraud={triage['fraud_risk']}"
    )

    action_list = []

    for _, playbook in playbooks.iterrows():

        action_list.append(
            playbook["ActionDescription"]
        )

        create_action(
            conn,
            claim["ClaimID"],
            playbook["ActionDescription"]
        )

    supplier_required = any(
        str(row["SupplierRequired"]).lower() == "yes"
        for _, row in playbooks.iterrows()
    )

    if supplier_required:

        supplier = recommend_supplier(
            claim,
            triage
        )

        assign_supplier(
            conn,
            claim["ClaimID"],
            supplier["supplier"]
        )

    else:

        supplier = {
            "supplier": "Not Required",
            "reason": "Playbook does not require supplier"
        }

    conn.commit()
    conn.close()

    return {
        "ClaimID": claim["ClaimID"],
        "Priority": triage["priority"],
        "FraudRisk": triage["fraud_risk"],
        "Actions": action_list,
        "Supplier": supplier["supplier"],
        "Reason": supplier["reason"]
    }
    



# ==================================================
# STREAMLIT UI
# ==================================================

st.set_page_config(
    page_title="Claims Agent",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Claims Agent designed by RoseTechCyber")

#   claims_df = pd.read_csv("ClaimsData/claims_data.csv")
claims_df = get_all_claims()
claim_ids = claims_df["ClaimID"].tolist()

selected_claim = st.selectbox(
    "Select Claim",
    claim_ids
)

if st.button("Process Claim"):
    claim = claims_df[
        claims_df["ClaimID"] == selected_claim
    ].iloc[0].to_dict()

    result = process_claim(claim)
    context = get_claim_context(selected_claim)

    st.success("Claim Processed")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Triage Result")
        st.write("Priority:", result["Priority"])
        st.write("Fraud Risk:", result["FraudRisk"])

        st.write("Recommended Actions")
        for action in result["Actions"]:
            st.write("✅", action)
     
        st.subheader("Notes")
        st.dataframe(context["notes"]) 
         
        st.subheader("Actions")
        st.dataframe(context["actions"])
         
        st.subheader("Assignments")
        st.dataframe(context["assignments"])
         
    with col2:
        st.subheader("Supplier Recommendation")
        st.write("Supplier:", result["Supplier"])
        st.write("Reason:", result["Reason"])

    st.subheader("Final Recommendation")

    st.json(result)