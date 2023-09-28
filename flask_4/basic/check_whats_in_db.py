import sqlite3
conn = sqlite3.connect("people.db")

cur = conn.cursor()
cur.execute("SELECT * FROM person")

people = cur.fetchall()
for person in people:
    print(person)


cur = conn.cursor()
cur.execute("SELECT * FROM note")

notes = cur.fetchall()
for note in notes:
    print(note)