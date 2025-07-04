from flask_restx import fields
from app.extensions import api

subscription_model = api.model("Subscription", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer,
    "subscription_plan_id": fields.Integer,
    "status": fields.String,
    "start_date": fields.DateTime,
    "end_date": fields.DateTime,
    "renewal_date": fields.DateTime,
    "auto_renew": fields.Boolean
})

subscription_input_model = api.model("SubscriptionInput", {
    "user_id": fields.Integer(required=True),
    "subscription_plan_id": fields.Integer(required=True),
    "status": fields.String(required=True, example="subscribed"),
    "start_date": fields.DateTime(required=True),
    "end_date": fields.DateTime(required=True),
    "renewal_date": fields.DateTime(required=True),
    "auto_renew": fields.Boolean(default=False)
})
