from datetime import datetime
from config import app, db
from models import Person, Comment, Task

PEOPLE_TASKS_COMMENTS = [
    {
        "lname": "Fairy",
        "fname": "Tooth",
        "tasks": [
                    {
                        "name": "First task",
                        "comments": [
                                    ("Resonable", "2022-01-06 17:10:24"),
                                    ("Use hummer", "2022-03-05 22:17:54"),
                                    ("Do you pay per gram?", "2022-03-05 22:18:10"),
                                ],
                        "timestamp": "2022-12-30 10:22:27"
                    },
        ],
    },
    {
        "lname": "Ruprecht",
        "fname": "Knecht",
        "tasks": [
                    {
                        "name": "First task",
                        "comments": [
                                    ("Two years late", "2022-01-07 22:47:54"),
                                    ("No need", "2022-04-06 13:03:17"),
                                ],
                        "timestamp": "2020-11-26 13:50:03"
                    },
        ]
    },
    {
        "lname": "Bunny",
        "fname": "Easter",
        "tasks": [
                    {
                        "name": "Second task",
                        "comments": [
                                    ("Too late for that", "2022-01-07 22:47:54"),
                                    ("No need to hide the eggs this time.", "2022-04-06 13:03:17"),
                                ],
                        "timestamp": "2021-06-09 14:00:00"
                    },
                    {
                        "name": "First task",
                        "comments": [
                                    ("Too late for that", "2022-01-07 22:47:54"),
                                    ("No need to hide the eggs this time.", "2022-04-06 13:03:17"),
                                ],
                        "timestamp": "2021-05-06 14:00:00"
                    },
        ],
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in PEOPLE_TASKS_COMMENTS:
        new_person = Person(lname=data.get("lname"), fname=data.get("fname"))
        for task in data.get('tasks'):
            new_task = Task(name = task.get('name'), timestamp = datetime.strptime(task.get('timestamp'), "%Y-%m-%d %H:%M:%S"))
            for content, times in task.get('comments'):
                new_task.comments.append(
                    Comment(
                        content = content,
                        timestamp=datetime.strptime(times, "%Y-%m-%d %H:%M:%S")
                    )
                )
            new_person.tasks.append(new_task)
        db.session.add(new_person)
    db.session.commit()
