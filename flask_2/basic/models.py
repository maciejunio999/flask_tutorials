from datetime import datetime
from config import db, ma

# inheriting from db.Model gives Person the SQLAlchemy features to connect to the database and access its tables
class Person(db.Model):
    # connects the class definition to the person database table
    __tablename__ = "person"
    # show structure of table as class field
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

# defines how the attributes of a class will be converted into JSON-friendly formats
class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # this is how Marshmallow finds attributes in the Person class and learns the types of those attributes so it knows how to serialize and deserialize them
        model = Person
        # ables to deserialize JSON data and load Person model instances from it
        load_instance = True
        sqla_session = db.session

person_schema = PersonSchema()
people_schema = PersonSchema(many=True)