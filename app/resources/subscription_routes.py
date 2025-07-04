from flask import request
from werkzeug.exceptions import NotFound
from flask_restx import Resource, Namespace, abort
from app.models.subscription import Subscription
from app.extensions import db
from app.api_models.subscription_models import subscription_model, subscription_input_model

sub = Namespace("Subscription", path="/api",
                description="Subscription management")


@sub.route("/subscriptions")
class SubscriptionListAPI(Resource):
    # marshal_list_with is used to convert the list of courses to the Course model
    # mauunang kunin yung return results, tsaka pupunta sa marshal
    @sub.marshal_list_with(subscription_model)
    def get(self):
        return Subscription.query.all()

    @sub.expect(subscription_input_model)
    @sub.marshal_with(subscription_model)
    def post(self):
        data = request.json
        subscription = Subscription(
            user_id=data["user_id"],
            subscription_plan_id=data["subscription_plan_id"],
            status=data["status"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            renewal_date=data["renewal_date"],
            auto_renew=data.get("auto_renew", False)
        )
        db.session.add(subscription)
        db.session.commit()
        return subscription, 201


@sub.route("/subscriptions/<int:id>")
class SubscriptionAPI(Resource):

    @sub.marshal_with(subscription_model)
    def get(self, id):
        subscription = Subscription.query.get(id)
        if not subscription:
            abort(404, message=f"Subscription with ID {id} not found")
        return subscription

    @sub.expect(subscription_input_model)
    @sub.marshal_with(subscription_model)
    def put(self, id):
    
        subscription = Subscription.query.get(id)
        if not subscription:
            abort(404, message=f"Subscription with ID {id} not found")

        data = request.json

        subscription.user_id = data["user_id"]
        subscription.subscription_plan_id = data["subscription_plan_id"]
        subscription.status = data["status"]
        subscription.start_date = data["start_date"]
        subscription.end_date = data["end_date"]
        subscription.renewal_date = data["renewal_date"]
        subscription.auto_renew = data.get("auto_renew", False)
        db.session.commit()
        return subscription, 200

    def delete(self, id):
        subscription = Subscription.query.get(id)
        if not subscription:
            abort(404, message=f"Subscription with ID {id} not found")
        db.session.delete(subscription)
        db.session.commit()
        return {}, 204
