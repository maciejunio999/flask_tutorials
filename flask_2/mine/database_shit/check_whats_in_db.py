import sqlite3

conn_p = sqlite3.connect("people_and_tasks.db")
cur_p = conn_p.cursor()
cur_p.execute("SELECT * FROM person")

people = cur_p.fetchall()
for person in people:
    print(person)

print('='*20)

conn_t = sqlite3.connect("people_and_tasks.db")
cur_t = conn_t.cursor()
cur_t.execute("SELECT * FROM tasks")


tasks = cur_t.fetchall()
for task in tasks:
    print(task)