from flask import request 
from werkzeug.exceptions import NotFound
from flask_restx import Resource, Namespace, abort
from app.models.users import User
from app.extensions import db
from app.api_models.users_models import user_model, user_input_model

usr = Namespace("User", path="/api/v1", description="User management")


@usr.route("/users")
class UserListAPI(Resource):
    #marshal_list_with is used to convert the list of courses to the Course model
    #mauunang kunin yung return results, tsaka pupunta sa marshal
    @usr.marshal_list_with(user_model)
    def get(self):
        return User.query.all()
    
    @usr.expect(user_input_model)
    @usr.marshal_with(user_model)
    def post(self):
        data = request.json
        user = User(
            email=data["email"],
            username=data["username"],
            phone=data["phone"]
        )
        db.session.add(user)
        db.session.commit()
        return user, 201
          
@usr.route("/users/<int:id>")
class UserAPI(Resource):
    @usr.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message=f"User with ID {id} not found")
        return user

    @usr.expect(user_input_model)
    @usr.marshal_with(user_model)
    def put(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message=f"User with ID {id} not found")
        data = request.json
        user.email = data["email"]
        user.username = data["username"]
        user.phone = data["phone"]
        db.session.commit()
        return user, 200

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message=f"User with ID {id} not found")
        db.session.delete(user)
        db.session.commit()
        return {}, 204