from flask_restx import fields
from app.extensions import api


user_model = api.model("User", {
    "id": fields.Integer(readonly=True),
    "email": fields.String,
    "username": fields.String,
    "phone": fields.String
})

user_input_model = api.model("UserInput", {
    "email": fields.String(required=True),
    "username": fields.String(required=True),
    "phone": fields.String
})
