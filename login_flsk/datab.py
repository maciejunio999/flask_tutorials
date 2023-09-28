from app import app
from app import db
import os
import shutil


def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            f = os.path.join(root, name).replace('\\', '/')
            result.append(f)
    return result

def trash_old_database(paths, name):
    for path in paths:
        path.replace(name, "")
        shutil.rmtree(path)
        os.rmdir(path)

name = 'database.db'
l = find_all(name, "C:/Users/maciej.antosz/Desktop/priv/login_flsk")

if len(l) == 0:
    with app.app_context():
        db.create_all()
else:
    print("Delete old database and run again")