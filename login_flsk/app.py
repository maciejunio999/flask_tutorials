from flask import Flask, render_template, url_for, redirect, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'this_key'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class Nick(db.Model):
    id_users = db.Column(db.Integer, primary_key=True, nullable=False)
    nickname = db.Column(db.String(50), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class NickForm(FlaskForm):
    nickname = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Nickname"})
    submit = SubmitField("Set nick")


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = NickForm()
    
    if current_user.id > 0:
        if form.validate_on_submit():
            new_nickname = Nick(id_users=current_user.id, nickname=form.nickname.data)
            db.session.add(new_nickname)
            db.session.commit()
            return redirect(url_for('dashboard'))

    try:
        nick = Nick.query.filter_by(id_users=current_user.id).first().nickname
    except AttributeError:
        nick=""
    if len(nick) > 0:
        return render_template('dashboard.html', form=form, nickname=nick)
    else:
        return render_template('dashboard.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5050)