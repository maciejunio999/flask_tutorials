#
# handles API requests for comments
#

from flask import abort, make_response
from config import db
from models import Comment, Task, comment_schema


def read_one(comment_id):
    comment = Comment.query.get(comment_id)

    if comment is not None:
        return comment_schema.dump(comment)
    else:
        abort(
            404, f"Note with ID {comment_id} not found"
        )


def update(comment_id, comment):
    existing_comment = Comment.query.get(comment_id)

    if existing_comment:
        update_comment = comment_schema.load(comment, session=db.session)
        existing_comment.content = update_comment.content
        db.session.merge(existing_comment)
        db.session.commit()
        return comment_schema.dump(existing_comment), 201
    else:
        abort(404, f"Comment with ID {comment_id} not found")


def delete(comment_id):
    existing_comment = Comment.query.get(comment_id)

    if existing_comment:
        db.session.delete(existing_comment)
        db.session.commit()
        return make_response(f"{comment_id} successfully deleted", 204)
    else:
        abort(404, f"Comment with ID {comment_id} not found")


def create(comment):
    task_id = comment.get("task_id")
    task = Task.query.get(task_id)

    if task:
        new_comment = comment_schema.load(comment, session=db.session)
        task.comments.append(new_comment)
        db.session.commit()
        return comment_schema.dump(new_comment), 201
    else:
        abort(
            404,
            f"Task not found for ID: {task_id}"
        )
