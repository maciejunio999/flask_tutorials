#
# defines database structure
#

from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy import fields

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        # model contains a foreign key, you must
        include_fk = True

# inheriting from db.Model gives Person the SQLAlchemy features to connect to the database and access its tables
class Person(db.Model):
    # connects the class definition to the person database table
    __tablename__ = "person"
    # show structure of table as class field
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), nullable=False)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    # this object creates the relationship that you’re adding to the Person class, and it’s created with all of the parameters defined in the lines that follow
    notes = db.relationship(
        # defines the SQLAlchemy class that the Person class will be related to
        Note,
        # backwards reference
        backref="person",
        # parameter determines how to treat Note instances when changes are made to the parent Person instance
        cascade="all, delete, delete-orphan",
        #  parameter is required if delete-orphan is part of the previous cascade parameter. This tells SQLAlchemy not to allow an orphaned Note instance
        single_parent=True,
        order_by="desc(Note.timestamp)"
    )

# defines how the attributes of a class will be converted into JSON-friendly formats
class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # this is how Marshmallow finds attributes in the Person class and learns the types of those attributes so it knows how to serialize and deserialize them
        model = Person
        # ables to deserialize JSON data and load Person model instances from it
        load_instance = True
        sqla_session = db.session
        # tell Marshmallow to add any related objects to the person schema
        include_relationships = True
    
    notes = fields.Nested(NoteSchema, many=True)


person_schema = PersonSchema()
people_schema = PersonSchema(many=True)

note_schema = NoteSchema()