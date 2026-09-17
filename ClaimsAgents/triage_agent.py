def calculate_fraud_score(claim, notes):

    fraud_score = 0

    if str(
        claim["MultipleRecentClaims"]
    ).lower() == "true":

        fraud_score += 2

    if float(
        claim["EstimatedLoss"]
    ) > 50000:

        fraud_score += 2

    if not notes.empty:

        fraud_notes = notes[
            notes["IsFraudRelated"] == 1
        ]

        fraud_score += len(fraud_notes)

    return fraud_score


def assess_claim(claim, notes):

    estimated_loss = float(
        claim["EstimatedLoss"]
    )

    claim_type = claim["ClaimType"]

    if estimated_loss > 10000:

        priority = "High"

    elif estimated_loss >= 5000:

        priority = "Medium"

    else:

        priority = "Low"

    fraud_score = calculate_fraud_score(
        claim,
        notes
    )

    if fraud_score >= 4:

        fraud_risk = "High"

    elif fraud_score >= 2:

        fraud_risk = "Medium"

    else:

        fraud_risk = "Low"

    return {
        "claim_type": claim_type,
        "priority": priority,
        "fraud_risk": fraud_risk,
    }