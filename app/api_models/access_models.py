from flask_restx import fields
from app.extensions import api

access_continuity_model = api.model("AccessContinuity", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer,
    "product_id": fields.Integer,
    "subscription_id": fields.Integer,
    "has_access": fields.Boolean,
    "expires_at": fields.Date
})

access_continuity_input_model = api.model("AccessContinuityInput", {
    "user_id": fields.Integer(required=True),
    "product_id": fields.Integer(required=True),
    "subscription_id": fields.Integer,
    "has_access": fields.Boolean(required=True),
    "expires_at": fields.Date(required=True)
})