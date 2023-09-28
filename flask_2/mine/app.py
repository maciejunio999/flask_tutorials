from flask import render_template
import config
from models import Person, Task

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    people = Person.query.all()
    tasks = Task.query.all()
    return render_template("home.html", people=people, tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)