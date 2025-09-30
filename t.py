from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.String(20), nullable=True)
    priority = db.Column(db.String(10), default="Medium")
    completed = db.Column(db.Boolean, default=False)

@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/tasks/add", methods=["POST"])
def add_task():
    task = Task(
        title=request.form["title"],
        description=request.form.get("description"),
        due_date=request.form.get("due_date"),
        priority=request.form.get("priority", "Medium")
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/tasks/delete/<int:id>", methods=["POST"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/tasks/complete/<int:id>", methods=["POST"])
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
