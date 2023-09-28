from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    s = False
    if request.method == 'POST':
        task_name = request.form['name'].strip()
        task_description = request.form['description'].strip()
        task_due_date = request.form['due_date'].strip()
        if len(task_name) > 0:
            new_task = Todo(name=task_name, description=task_description, due_date=task_due_date)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
        elif len(task_name) == 0:
            s = True
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('index.html', tasks=tasks, show_hidden=s)
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks, show_hidden=s)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting that task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    s = False

    if request.method == 'POST':
        task_to_update.name = request.form['name'].strip()
        task_to_update.description = request.form['description'].strip()
        task_to_update.due_date = request.form['due_date'].strip()
        if len(task_to_update.name) > 0:
            try:
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue updating that task"
        else:
            s = True
            return render_template('update.html', task=task_to_update, show_hidden=s)
    else:
        return render_template('update.html', task=task_to_update)

if __name__ == "__main__":
    app.run(debug=True)