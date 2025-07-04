from flask_restx import fields
from app.extensions import api

payment_model = api.model("Payment", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer(required=True),
    "subscription_id": fields.Integer(required=True),
    "amount": fields.Float(required=True),
    "payment_method": fields.String(required=True),
    "paid_at": fields.DateTime,
    "status": fields.String,
    "transaction_id": fields.String
})

payment_input_model = api.model("PaymentInput", {
    "user_id": fields.Integer(required=True),
    "subscription_id": fields.Integer(required=True),
    "amount": fields.Float(required=True),
    "payment_method": fields.String(required=True),
    "transaction_id": fields.String(required=False)
})
