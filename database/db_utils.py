import sqlite3
import pandas as pd

DB_NAME = "database/claims.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def get_all_claims():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM Claims
        ORDER BY date(SubmissionDate) DESC
        """,
        conn
    )

    conn.close()

    return df


def get_claim_context(claim_id):

    conn = get_connection()

    claim = pd.read_sql_query(
        """
        SELECT *
        FROM Claims
        WHERE ClaimID = ?
        """,
        conn,
        params=(claim_id,)
    )

    notes = pd.read_sql_query(
        """
        SELECT *
        FROM ClaimNotes
        WHERE ClaimID = ?
        ORDER BY NoteDate DESC
        """,
        conn,
        params=(claim_id,)
    )

    actions = pd.read_sql_query(
        """
        SELECT *
        FROM ClaimActions
        WHERE ClaimID = ?
        ORDER BY ActionDate DESC
        """,
        conn,
        params=(claim_id,)
    )

    assignments = pd.read_sql_query(
        """
        SELECT *
        FROM ClaimAssignments
        WHERE ClaimID = ?
        ORDER BY AssignedDate DESC
        """,
        conn,
        params=(claim_id,)
    )

    conn.close()

    return {
        "claim": claim,
        "notes": notes,
        "actions": actions,
        "assignments": assignments
    }