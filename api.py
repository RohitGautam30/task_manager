from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(20))
    priority = db.Column(db.String(10))
    status = db.Column(db.String(20), default="Pending")

    def __repr__(self):
        return f"<Task {self.title}>"


task_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "due_date": fields.String,
    "priority": fields.String,
    "status": fields.String,
}

task_args = reqparse.RequestParser()
task_args.add_argument("title", type=str, required=True, help="Title cannot be blank")
task_args.add_argument("description", type=str, required=True, help="Description cannot be blank")
task_args.add_argument("due_date", type=str)
task_args.add_argument("priority", type=str)
task_args.add_argument("status", type=str)


class Tasks(Resource):
    @marshal_with(task_fields)
    def get(self):
        tasks = TaskModel.query.all()
        return tasks

    @marshal_with(task_fields)
    def post(self):
        args = task_args.parse_args()
        task = TaskModel(
            title=args["title"],
            description=args["description"],
            due_date=args.get("due_date"),
            priority=args.get("priority"),
            status=args.get("status", "Pending"),
        )
        db.session.add(task)
        db.session.commit()
        return task, 201

class Task(Resource):
    @marshal_with(task_fields)
    def get(self, id):
        task = TaskModel.query.filter_by(id=id).first()
        if not task:
            abort(404, "Task not found")
        return task

    @marshal_with(task_fields)
    def patch(self, id):
        args = task_args.parse_args()
        task = TaskModel.query.filter_by(id=id).first()
        if not task:
            abort(404, "Task not found")
        if args["title"]:
            task.title = args["title"]
        if args["description"]:
            task.description = args["description"]
        if args["due_date"]:
            task.due_date = args["due_date"]
        if args["priority"]:
            task.priority = args["priority"]
        if args["status"]:
            task.status = args["status"]
        db.session.commit()
        return task

    def delete(self, id):
        task = TaskModel.query.filter_by(id=id).first()
        if not task:
            abort(404, "Task not found")
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted"}, 204


api.add_resource(Tasks, "/api/tasks/")
api.add_resource(Task, "/api/tasks/<int:id>")


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure DB + tables created
    app.run(debug=True)
