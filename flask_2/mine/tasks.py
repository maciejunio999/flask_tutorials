from flask import abort, make_response
from config import db
from models import Task, tasks_schema, task_schema

def read_all():
    tasks = Task.query.all()
    return tasks_schema.dump(tasks)

def create(task):
    name = task.get("name")
    existing_task = Task.query.filter(Task.name == name).one_or_none()

    if existing_task is None:
        new_task = task_schema.load(task, session=db.session)
        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task), 201
    else:
        abort(406, f"Person with last name {name} already exists")

def read_one(name):
    task = Task.query.filter(Task.name == name).one_or_none()

    if task is not None:
        return task_schema.dump(task)
    else:
        abort(404, f"Person with last name {name} not found")

def update(name, task):
    existing_task = Task.query.filter(Task.name == name).one_or_none()

    if existing_task:
        update_task = task_schema.load(task, session=db.session)
        existing_task.name = update_task.name
        existing_task.comment = update_task.comment
        existing_task.due_date = update_task.due_date
        db.session.merge(existing_task)
        db.session.commit()
        return task_schema.dump(existing_task), 201
    else:
        abort(404, f"Person with last name {name} not found")

def delete(name):
    existing_task = Task.query.filter(Task.name == name).one_or_none()

    if existing_task:
        db.session.delete(existing_task)
        db.session.commit()
        return make_response(f"{name} successfully deleted", 200)
    else:
        abort(404, f"Person with last name {name} not found")