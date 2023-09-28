from flask import abort, make_response

from config import db
from models import Task, Person, task_schema

def read_one(task_id):
    task = Task.query.get(task_id)

    if task is not None:
        return task_schema.dump(task)
    else:
        abort(
            404, f"Task with ID {task_id} not found"
        )

def update(person_id, task_id, task):
    existing_task = Task.query.get(task_id)
    person = Person.query.get(person_id)

    if existing_task and person:
        update_task = task_schema.load(task, session=db.session)
        existing_task.name = update_task.name
        db.session.merge(existing_task)
        db.session.commit()
        return task_schema.dump(existing_task), 201
    else:
        abort(404, f"Task with ID {task_id} not found")

def delete(task_id):
    existing_task = Task.query.get(task_id)

    if existing_task:
        db.session.delete(existing_task)
        db.session.commit()
        return make_response(f"{task_id} successfully deleted", 204)
    else:
        abort(404, f"Task with ID {task_id} not found")

def create(task):
    person_id = task.get("person_id")
    person = Person.query.get(person_id)

    if person:
        new_task = task_schema.load(task, session=db.session)
        person.tasks.append(new_task)
        db.session.commit()
        return task_schema.dump(new_task), 201
    else:
        abort(
            404,
            f"Person not found for ID: {person_id}"
        )