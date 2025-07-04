from flask_restx import fields
from app.extensions import api

access_continuity_model = api.model("AccessContinuity", {
    "user_id": fields.Integer,
    "product_id": fields.Integer,
    "subscription_id": fields.Integer,
    "has_access": fields.Boolean,
    "expires_at": fields.DateTime
})
