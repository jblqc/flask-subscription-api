from flask_restx import fields
from app.extensions import api

subscription_model = api.model("Subscription", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer,
    "subscription_plan_id": fields.Integer,
    "status": fields.String,
    "start_date": fields.DateTime,
    "end_date": fields.DateTime,
    "auto_renew": fields.Boolean
})

subscription_input_model = api.model("SubscriptionInput", {
    "user_id": fields.Integer(required=True),
    "subscription_plan_id": fields.Integer(required=True),
    "start_date": fields.DateTime,
    "end_date": fields.DateTime,
    "auto_renew": fields.Boolean(default=False)
})

subscription_per_user_model = api.model("SubscriptionPerUser", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer,
    "plan_id": fields.Integer,
    "username": fields.String,
    "status": fields.String,
    "start_date": fields.DateTime,
    "end_date": fields.DateTime,
    "auto_renew": fields.Boolean,
    "product_name": fields.String,
    "plan_name": fields.String,
    "frequency_duration_days": fields.Integer,
})