import sqlite3

conn = sqlite3.connect("wallets.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE wallet ADD COLUMN created_at DATETIME;")
cursor.execute("ALTER TABLE wallet ADD COLUMN updated_at DATETIME;")

cursor.execute("UPDATE wallet SET created_at = CURRENT_TIMESTAMP;")
cursor.execute("UPDATE wallet SET updated_at = CURRENT_TIMESTAMP;")

conn.commit()
conn.close()

