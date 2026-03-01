import sqlite3

conn = sqlite3.connect("tickets.db", check_same_thread=False)
cursor = conn.cursor()

def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    issue TEXT,
    priority TEXT,
    status TEXT
    )
    """)
    conn.commit()

def add_ticket(name,issue,priority):
    cursor.execute(
        "INSERT INTO tickets(name,issue,priority,status) VALUES (?,?,?,?)",
        (name,issue,priority,"Open")
    )
    conn.commit()

def view_tickets():
    cursor.execute("SELECT * FROM tickets")
    return cursor.fetchall()

def update_status(status,id):
    cursor.execute("UPDATE tickets SET status=? WHERE id=?",(status,id))
    conn.commit()
