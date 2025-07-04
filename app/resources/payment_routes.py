from flask_restx import Resource, Namespace, abort
from flask import request
from app.models.payment import Payment
from app.models.subscription import Subscription
from app.models.users import User
from app.extensions import db
from app.api_models.payment_models import payment_model, payment_input_model
from datetime import datetime

payment = Namespace("Payments", path="/api", description="Payment processing example")

@payment.route("/payments")
class PaymentListAPI(Resource):
    @payment.marshal_list_with(payment_model)
    def get(self):
        return Payment.query.all()

    @payment.expect(payment_input_model)
    @payment.marshal_with(payment_model)
    def post(self):
        data = request.json

        if not User.query.get(data["user_id"]):
            abort(400, message="Invalid user_id")
        if not Subscription.query.get(data["subscription_id"]):
            abort(400, message="Invalid subscription_id")

        new_payment = Payment(
            user_id=data["user_id"],
            subscription_id=data["subscription_id"],
            amount=data["amount"],
            payment_method=data["payment_method"],
            transaction_id=data.get("transaction_id"),
            status="paid",
            paid_at=datetime.utcnow()
        )
        db.session.add(new_payment)
        db.session.commit()
        return new_payment, 201

@payment.route("/payments/<int:id>")
class PaymentAPI(Resource):
    @payment.marshal_with(payment_model)
    def get(self, id):
        payment = Payment.query.get(id)
        if not payment:
            abort(404, message="Payment not found")
        return payment

    def delete(self, id):
        payment = Payment.query.get(id)
        if not payment:
            abort(404, message="Payment not found")
        db.session.delete(payment)
        db.session.commit()
        return {}, 204
