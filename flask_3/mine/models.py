from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy import fields



class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
        sqla_session = db.session
        include_fk = True



class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    comments = db.relationship(
        Comment,
        backref="task",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Comment.timestamp)"
    )

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        sqla_session = db.session
        include_fk = True
    comments = fields.Nested(CommentSchema, many=True)



class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    tasks = db.relationship(
        Task,
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Task.timestamp)"
    )

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True
    
    tasks = fields.Nested(TaskSchema, many=True)



person_schema = PersonSchema()
people_schema = PersonSchema(many=True)

task_schema = TaskSchema()

comment_schema = CommentSchema()