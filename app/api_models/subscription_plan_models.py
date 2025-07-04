from flask_restx import fields
from app.extensions import api

subscription_plan_model = api.model("SubscriptionPlan", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "product_id": fields.Integer(required=True),
    "frequency_option_id": fields.Integer(required=True)
})

subscription_plan_input_model = api.model("SubscriptionPlanInput", {
    "name": fields.String(required=True),
    "product_id": fields.Integer(required=True),
    "frequency_option_id": fields.Integer(required=True)
})
