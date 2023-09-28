from app import app, db, User, Nick

with app.app_context():
    for user in db.session.query(User):
        print(user.username)
    print("="*20)
    for nick in db.session.query(Nick):
       print(nick.nickname)