from . import db, api
from flask_restful import reqparse, Resource, fields, marshal_with, marshal, abort
from sqlalchemy.exc import IntegrityError

user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, required=True, help="Username is required", location='json')
user_args.add_argument("email", type=str, required=True, help="Email is required", location='json')

userfields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String
}

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    

class Users(Resource):
    @marshal_with(userfields)

    # Get all users
    def get(self):
        return UserModel.query.all()
    
    # Create a new user
    def post(self):
        args = user_args.parse_args()
        user = UserModel(username=args['username'], email=args['email'])
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message="Username or email already exists")
        return marshal(user, userfields), 201


class User(Resource):
    @marshal_with(userfields)
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")
        return user
    
    @marshal_with(userfields)
    def patch(self, user_id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")
        user.username = args['username']
        user.email = args['email']
        db.session.commit()
        return user
    
    @marshal_with(userfields)
    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return user
    
api.add_resource(Users, "/users")
api.add_resource(User, "/users/<int:user_id>")
