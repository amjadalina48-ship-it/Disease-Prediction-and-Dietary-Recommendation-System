import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Replace with the username and password you want
username = "user1"
password = "pass123"

cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
conn.commit()
conn.close()

print(f"User '{username}' added successfully!")