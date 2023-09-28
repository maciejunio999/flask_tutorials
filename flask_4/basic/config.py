#
# creates and initializes projects configuration
#

import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()

# create the Connexion app instance and give it the path to the directory that contains your specification file
connex_app = connexion.App(__name__, specification_dir=basedir)

# Flask instance initialized by Connexion
app = connex_app.app
# tell SQLAlchemy to use SQLite as the database and a file named people.db in the current directory as the database file
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'people.db'}"
# turns the SQLAlchemy event system off
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initializes SQLAlchemy by passing the app configuration information to SQLAlchemy and assigning the result to a db variable
db = SQLAlchemy(app)
# initializes Marshmallow and allows it to work with the SQLAlchemy components attached to the app
ma = Marshmallow(app)