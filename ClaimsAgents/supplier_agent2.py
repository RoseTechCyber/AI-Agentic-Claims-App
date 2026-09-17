import sqlite3
import pandas as pd

DB_NAME = "database/claims.db"


def load_suppliers():

    conn = sqlite3.connect(
        DB_NAME
    )

    df = pd.read_sql_query(
        """
        SELECT *
        FROM suppliers
        WHERE Active='Yes'
        """,
        conn
    )

    conn.close()

    return df


def recommend_supplier(claim, triage):

    suppliers = load_suppliers()

    matching = suppliers[
        (
            suppliers["Specialty"]
            .str.lower()
            ==
            claim["ClaimType"]
            .lower()
        )
        &
        (
            suppliers["Region"]
            .str.lower()
            ==
            claim["Region"]
            .lower()
        )
    ]

    if matching.empty:

        matching = suppliers[
            suppliers["Specialty"]
            .str.lower()
            ==
            claim["ClaimType"]
            .lower()
        ]

    if matching.empty:

        return {
            "supplier": "Manual Review",
            "reason": "No supplier found"
        }
        
    matching["PreferredScore"] = (
    matching["PreferredSupplier"]
    .str.lower()
    .eq("yes")
    .astype(int))

    best = matching.sort_values(
        by=[
            "PreferredSupplier",
            "PerformanceRating"
        ],
        ascending=False
    ).iloc[0]

    return {

        "supplier":
            best["SupplierName"],

        "supplier_id":
            best["SupplierID"],

        "rating":
            best["PerformanceRating"],

        "reason":
            f"Matched "
            f"{claim['ClaimType']} "
            f"claim in "
            f"{claim['Region']}"
    }