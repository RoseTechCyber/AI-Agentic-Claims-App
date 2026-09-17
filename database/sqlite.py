import sqlite3

conn = sqlite3.connect("claims.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO Claims_Playbooks
(
    ClaimType,
    Priority,
    FraudRisk,
    ActionType,
    ActionDescription,
    SupplierRequired,
    EscalationLevel,
    Active
)
VALUES
(
    'Property',
    'High',
     'Low',
     'Follow Up',
     'Assign Senior Adjuster',
     'Yes',
     'Manager',
     'Yes'
)

""")

cursor.execute("""
INSERT INTO Claims_Playbooks
(
    ClaimType,
    Priority,
    FraudRisk,
    ActionType,
    ActionDescription,
    SupplierRequired,
    EscalationLevel,
    Active
)
VALUES
(
   'Property',
   'High',
   'High',
   'Fast Track',
   'Refer to SIU',
   'No',
   'Fraud',
   'Yes'
)
""")

cursor.execute("""
INSERT INTO Claims_Playbooks
(
    ClaimType,
    Priority,
    FraudRisk,
    ActionType,
    ActionDescription,
    SupplierRequired,
    EscalationLevel,
    Active
)
VALUES
(
    'Motor',
    'Low',
    'Low',
    'FastTrack',
    'Proceed with low-value settlement',
    'No',
    'None',
    'Yes'
);
""")

cursor.execute("""
INSERT INTO Claims_Playbooks
(
    ClaimType,
    Priority,
    FraudRisk,
    ActionType,
    ActionDescription,
    SupplierRequired,
    EscalationLevel,
    Active
)
VALUES
(
  'Motor',
   'Low',
   'Low',
   'Fast Track',
   'Fast Track Settlement',
   'No',
   'None',
   'Yes'
)
""")

conn.commit()
conn.close()