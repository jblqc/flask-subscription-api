from flask import request
from werkzeug.exceptions import NotFound
from flask_restx import Resource, Namespace, abort
from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan
from app.models.frequency_option import FrequencyOption

from app.extensions import db
from app.api_models.subscription_models import subscription_model, subscription_input_model, subscription_per_user_model
from datetime import datetime, timedelta

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
        
        subscription_plan = SubscriptionPlan.query.get(data["subscription_plan_id"])
        option_id = subscription_plan.frequency_option_id
        duration = FrequencyOption.query.get(option_id).duration_days
        
        subscription = Subscription(
            user_id=data["user_id"],
            subscription_plan_id=data["subscription_plan_id"],
            status="subscribed",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=duration),
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

@sub.route("/subscriptions/user/<int:user_id>")

class UserSubscriptionsAPI(Resource):
    @sub.marshal_with(subscription_per_user_model)
    def get(self, user_id):
        subscriptions = Subscription.query.filter_by(user_id=user_id).all()

        if not subscriptions:
            return {"message": f"No subscriptions found for user ID {user_id}"}, 404

        result = []
        for sub in subscriptions:
            plan = sub.subscription_plan
            product = plan.product if plan else None
            user = sub.user

            result.append({
                "id": sub.id,
                "plan_id": plan.id,
                "user_id": user.id,
                "username": user.username,
                "status": sub.status,
                "start_date": sub.start_date.isoformat(),
                "end_date": sub.end_date.isoformat(),
                "auto_renew": sub.auto_renew,
                "product_name": product.name if product else None,
                "plan_name": plan.name if plan else None,
                "frequency_duration_days": plan.frequency_option.duration_days if plan and plan.frequency_option else None,
            })

        return result, 200
