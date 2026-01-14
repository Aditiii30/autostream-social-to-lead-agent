import sqlite3
import json

DB_FILE = "leads.db"
JSON_FILE = "leads.json"

def mock_lead_capture(name, email, platform):
    # 1️⃣ Connect to SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 2️⃣ Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            platform TEXT NOT NULL
        )
    """)

    # 3️⃣ Insert lead into SQL database
    cursor.execute(
        "INSERT INTO leads (name, email, platform) VALUES (?, ?, ?)",
        (name, email, platform)
    )

    conn.commit()

    # 4️⃣ Read all leads from SQL
    cursor.execute("SELECT name, email, platform FROM leads")
    rows = cursor.fetchall()

    conn.close()

    # 5️⃣ Convert SQL rows to JSON format
    leads = []
    for row in rows:
        leads.append({
            "name": row[0],
            "email": row[1],
            "platform": row[2]
        })

    # 6️⃣ Save JSON file (readable layer)
    with open(JSON_FILE, "w") as f:
        json.dump(leads, f, indent=4)

    print(f"Lead captured successfully: {name}, {email}, {platform}")
