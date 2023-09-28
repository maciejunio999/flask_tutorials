import sqlite3

conn = sqlite3.connect("people_and_tasks.db")

columns_people = [
    "id INTEGER PRIMARY KEY",
    "lname VARCHAR UNIQUE",
    "fname VARCHAR",
    "timestamp DATETIME",
]

columns_tasks = [
    "id INTEGER PRIMARY KEY",
    "name VARCHAR UNIQUE",
    "comment VARCHAR",
    "due_date VARCHAR",
]

create_table_cmd = f"CREATE TABLE person ({','.join(columns_people)})"

conn.execute(create_table_cmd)

create_table_cmd = f"CREATE TABLE tasks ({','.join(columns_tasks)})"

conn.execute(create_table_cmd)

people = [
    "1, 'Maciej', 'Antosz', '2000-10-03 05:45:00'",
    "2, 'Julia', 'Petrov', '2021-09-02 22:47:33'",
    "3, 'Lena', 'Antosz', '2013-01-26 04:35:17'",
]

tasks = [
    "1, 'task1', 'Antosz', '2023-10-03'",
    "2, 'task2', 'Petrov', '2023-10-02'",
    "3, 'task3', 'Antosz', '2023-10-26'",
]

for person_data in people:
    insert_cmd = f"INSERT INTO person VALUES ({person_data})"
    conn.execute(insert_cmd)

for task in tasks:
    insert_cmd = f"INSERT INTO tasks VALUES ({task})"
    conn.execute(insert_cmd)

conn.commit()