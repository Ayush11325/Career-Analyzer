import sqlite3

conn = sqlite3.connect('careers.db')
cursor = conn.cursor()

# Table se data nikalna
cursor.execute("SELECT * FROM job_roles")
rows = cursor.fetchall()

print("ID | Role | Required Skills")
print("-" * 50)
for row in rows:
    print(f"{row[0]} | {row[1]} | {row[2]}")

conn.close()