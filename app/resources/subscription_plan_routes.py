from flask import request
from werkzeug.exceptions import NotFound
from flask_restx import Resource, Namespace, abort
from app.models.subscription_plan import SubscriptionPlan
from app.models.product import Product
from app.models.frequency_option import FrequencyOption
from app.extensions import db
from app.api_models.subscription_plan_models import subscription_plan_model, subscription_plan_input_model

subsplan = Namespace("Subscription Plan", path="/api",
                description="Subscription plan management")


@subsplan.route("/subscription_plans")
class SubscriptionListAPI(Resource):
    # marshal_list_with is used to convert the list of courses to the Course model
    # mauunang kunin yung return results, tsaka pupunta sa marshal
    @subsplan.marshal_list_with(subscription_plan_model)
    def get(self):
        return SubscriptionPlan.query.all()

    @subsplan.expect(subscription_plan_input_model)
    @subsplan.marshal_with(subscription_plan_model)
    def post(self):
        data = request.json
        # Validate product_id
        product = Product.query.get(data["product_id"])
        if not product:
            abort(400, message="Product ID does not exist")

        # Validate frequency_option_id
        freq_option = FrequencyOption.query.get(data["frequency_option_id"])
        if not freq_option:
            abort(400, message="Frequency Option ID does not exist")


        subscription_plan = SubscriptionPlan(
            name = data["name"],
            plan_price = data["plan_price"],
            product_id = data["product_id"],
            frequency_option_id = data["frequency_option_id"]
        )
        db.session.add(subscription_plan)
        db.session.commit()
        return subscription_plan, 201


@subsplan.route("/subscription_plans/<int:id>")
class SubscriptionAPI(Resource):
    
    @subsplan.marshal_with(subscription_plan_model)
    def get(self, id):
        subscription_plan = SubscriptionPlan.query.get(id)
        if not subscription_plan:
            abort(404, message=f"Subscription plan with ID {id} not found")
        return subscription_plan
    
    @subsplan.expect(subscription_plan_input_model)
    @subsplan.marshal_with(subscription_plan_model)
    def put(self, id):
        subscription_plan = SubscriptionPlan.query.get(id)
        if not subscription_plan:
            abort(404, message=f"Subscription plan with ID {id} not found")

        data = request.json
        product = Product.query.get(data["product_id"])
        if not product:
            abort(400, message=f"Invalid product_id: {data['product_id']}")

        freq_option = FrequencyOption.query.get(data["frequency_option_id"])
        if not freq_option:
            abort(400, message=f"Invalid frequency_option_id: {data['frequency_option_id']}")

        subscription_plan.name = data["name"]
        subscription_plan.product_id = data["product_id"]
        subscription_plan.plan_price = data["plan_price"]
        subscription_plan.frequency_option_id = data["frequency_option_id"]
        db.session.commit()
        return subscription_plan, 200

    def delete(self, id):
        subscription_plan = SubscriptionPlan.query.get(id)
        if not subscription_plan:
            abort(404, message=f"Subscription plan with ID {id} not found")

        db.session.delete(subscription_plan)
        db.session.commit()
        return {}, 204
