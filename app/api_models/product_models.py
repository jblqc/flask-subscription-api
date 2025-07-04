from flask_restx import fields
from app.extensions import api

product_model = api.model("Product", {
    "id": fields.Integer,
    "name": fields.String,
    "price": fields.Float,
    "description":fields.String,
    "is_active":fields.Boolean
})



product_input_model = api.model("ProductInput", {
    "name": fields.String,
    "price": fields.Float,
    "description":fields.String,
    "is_active":fields.Boolean
})