import pandas as pd


def recommend_supplier(claim, triage):

    suppliers = pd.read_csv(
        "ClaimsData/suppliers.csv"
    )

    matching = suppliers[
        (suppliers["Specialty"].str.lower()
         == claim["ClaimType"].lower())
        &
        (suppliers["Region"].str.lower()
         == claim["Region"].lower())
    ]

    if matching.empty:

        matching = suppliers[
            suppliers["Specialty"].str.lower()
            == claim["ClaimType"].lower()
        ]

    if matching.empty:
        return {
            "supplier": "Manual Review",
            "reason": "No supplier available"
        }

    best = matching.sort_values(
        by=["PerformanceRating"],
        ascending=False
    ).iloc[0]

    return {
        "supplier": best["SupplierName"],
        "supplier_id": best["SupplierID"],
        "rating": best["PerformanceRating"],
        "reason":
            f"Matched {claim['ClaimType']} "
            f"claim in {claim['Region']}"
    }