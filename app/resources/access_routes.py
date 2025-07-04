from flask import request
from flask_restx import Resource, Namespace, abort
from app.models.access_continuity import AccessContinuity
from app.api_models.access_models import access_continuity_model
from datetime import datetime
access = Namespace("Access Continuity", path="/api/v1", description="Access continuity management")


@access.route("/access")
class AccessListAPI(Resource):
    @access.doc(params={
        'user_id': 'Optional filter by user ID',
        'product_id': 'Optional filter by product ID'
    })
    @access.marshal_list_with(access_continuity_model)
    def get(self):
        user_id = request.args.get("user_id", type=int)
        product_id = request.args.get("product_id", type=int)

        from app.models.subscription import Subscription

        results = []
        subscriptions = Subscription.query.all()

        for sub in subscriptions:
            if not sub.subscription_plan or not sub.subscription_plan.product:
                continue

            product = sub.subscription_plan.product
            user = sub.user

            if user_id and user.id != user_id:
                continue
            if product_id and product.id != product_id:
                continue
            #check access continuity 
            has_access = sub.status.lower() == "subscribed" and sub.end_date > datetime.utcnow()

            results.append({
                "user_id": user.id,
                "product_id": product.id,
                "subscription_id": sub.id,
                "has_access": has_access,
                "expires_at": sub.end_date
            })

        if not results:
            abort(404, message="No access continuity records found.")

        return results
