from flask import request
from werkzeug.exceptions import NotFound
from flask_restx import Resource, Namespace, abort
from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan
from app.models.frequency_option import FrequencyOption
from app.logic.subscription import renew_subscription, cancel_subscription, expire_subscription
from app.models.payment import Payment
from app.models.users import User

from app.extensions import db
from app.api_models.subscription_models import subscription_model, subscription_input_model, subscription_per_user_model
from datetime import datetime, timedelta

sub = Namespace("Subscription", path="/api/v1",description="Subscription management")


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
        plan_price = subscription_plan.plan_price or 0.0
        # --- Validate: User can't subscribe to 2 plans of same product
        # Get all the subscription plans for the product for a user
        # Only get the Subscription plan based on the input id
        existing_sub = (
            db.session.query(Subscription)
            .join(SubscriptionPlan, Subscription.subscription_plan_id == SubscriptionPlan.id)
            .filter(
                Subscription.user_id == data["user_id"],
                SubscriptionPlan.product_id == subscription_plan.product_id,
                Subscription.status.in_(["subscribed"])
            )
            .first()
        )

        if existing_sub:
            abort(409, message="User is already subscribed to a plan for this product.")

        
        # ---- Step 1: Simulate payment creation (assume success for now)
        payment = Payment(
            user_id=data["user_id"],
            subscription_id=None,  # NO SUBSCRIPTION ID YET, subscription id will only generate upon succesfull subscription creation
            # In a real scenario, you would integrate with a payment gateway here
            payment_method="credit_card",  # placeholder
            transaction_id=f"transac_{datetime.utcnow().timestamp()}",
            amount=plan_price,
            status="success"
        )
        db.session.add(payment)

        if payment.status != "success":
            abort(403, message="Payment failed. Subscription not created.")

        # ---- Step 2: Create the subscription
        subscription = Subscription(
            user_id=data["user_id"],
            subscription_plan_id=data["subscription_plan_id"],
            status="subscribed",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=duration),
            auto_renew=data.get("auto_renew", False)
        )
        db.session.add(subscription)
        db.session.flush()

        # ---- Step 3: Update the payment record with the subscription ID
        payment.subscription_id = subscription.id
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
        try:
            # Convert ISO strings to datetime objects
            start_date = datetime.fromisoformat(data["start_date"].replace("Z", "+00:00"))
            end_date = datetime.fromisoformat(data["end_date"].replace("Z", "+00:00"))
        except Exception as e:
            abort(400, message=f"Invalid date format: {e}")

        subscription.user_id = data["user_id"]
        subscription.subscription_plan_id = data["subscription_plan_id"]
        subscription.start_date = start_date          
        subscription.end_date = end_date             
        subscription.auto_renew = data.get("auto_renew", False)
        if subscription.end_date < datetime.utcnow():
            subscription.status = "expired"
        else:
            subscription.status = "subscribed"
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
                "start_date": sub.start_date,  
                "end_date": sub.end_date,      
                "auto_renew": sub.auto_renew,
                "product_name": product.name if product else None,
                "plan_name": plan.name if plan else None,
                "frequency_duration_days": plan.frequency_option.duration_days if plan and plan.frequency_option else None,
            })

        return result, 200
    
    

@sub.route("/subscriptions/<int:id>/renew")
class SubscriptionRenewalAPI(Resource):
    def post(self, id):
        return renew_subscription(id)
    
@sub.route("/subscriptions/<int:id>/cancel")
class SubscriptionCancelAPI(Resource):
    def post(self, id):
        return cancel_subscription(id)


@sub.route("/subscriptions/<int:id>/expire")
class SubscriptionExpireAPI(Resource):
    def post(self, id):
        return expire_subscription(id)
