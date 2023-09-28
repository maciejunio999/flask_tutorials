import sqlite3
conn = sqlite3.connect("people.db")
cur = conn.cursor()


print('='*225)

cur.execute("SELECT * FROM person")

people = cur.fetchall()
for person in people:
    print(person)


print('='*225)

cur.execute("SELECT * FROM task")

tasks = cur.fetchall()
for task in tasks:
    print(task)


print('='*225)

cur.execute("SELECT * FROM comment")

comments = cur.fetchall()
for comment in comments:
    print(comment)