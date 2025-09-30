from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, marshal_with, fields, reqparse,abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True, help='Name is required')
user_parser.add_argument('email', type=str, required=True, help='Email is required')

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

class Hello(Resource):
    @marshal_with(resource_fields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(resource_fields)
    def post(self):
        args = user_parser.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201


class hey(Resource):
    @marshal_with(resource_fields)
    def get(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "user not found")
        return user
    
    @marshal_with(resource_fields)
    def patch(self,id):
        args = user_parser.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "user not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user

    @marshal_with(resource_fields)
    def delete(self,id):
        args = user_parser.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "user not found")
        db.session.delete(user)
        db.session.commit()
        return user,204
        

api.add_resource(Hello, "/hello")

if __name__ == "__main__":
    app.run(debug=True)
