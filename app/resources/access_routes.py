
from flask import request
from werkzeug.exceptions import NotFound
from flask_restx import Resource, Namespace, abort
from app.models.access_continuity import AccessContinuity
from app.models.users import User
from app.models.product import Product
from app.models.subscription import Subscription
from app.extensions import db
from app.api_models.access_models import access_continuity_model, access_continuity_input_model

access = Namespace("Access Continuity", path="/api", description="Access continuity management")

@access.route("/access")
class AccessListAPI(Resource):
    #marshal_list_with is used to convert the list of courses to the Course model
    #mauunang kunin yung return results, tsaka pupunta sa marshal
    @access.marshal_list_with(access_continuity_model)
    def get(self):
        return AccessContinuity.query.all()
    
    @access.expect(access_continuity_input_model)
    @access.marshal_with(access_continuity_model)
    def post(self):
        data = request.json
         # Foreign key validation
        if not User.query.get(data["user_id"]):
            abort(400, message=f"Invalid user_id: {data['user_id']}")
        if not Product.query.get(data["product_id"]):
            abort(400, message=f"Invalid product_id: {data['product_id']}")
        if not Subscription.query.get(data["subscription_id"]):
            abort(400, message=f"Invalid subscription_id: {data['subscription_id']}")

        access_continuity = AccessContinuity(
            user_id=data["user_id"],
            product_id=data["product_id"],
            subscription_id=data["subscription_id"],
            has_access=data["has_access"],
            expires_at=data["expires_at"]
        )
        db.session.add(access_continuity)
        db.session.commit()
        return access_continuity, 201
        
        
@access.route("/access/<int:id>")
class AccessAPI(Resource):
    @access.marshal_with(access_continuity_model)
    def get(self, id):
        access_continuity = AccessContinuity.query.get(id)
        if not access_continuity:
            abort(404, message=f"Access continuity with ID {id} not found")
        return access_continuity

    @access.expect(access_continuity_input_model)
    @access.marshal_with(access_continuity_model)
    def put(self, id):
        access_continuity = AccessContinuity.query.get(id)
        if not access_continuity:
            abort(404, message=f"Access continuity with ID {id} not found")
        data = request.json
         # Foreign key validation
        if not User.query.get(data["user_id"]):
            abort(400, message=f"Invalid user_id: {data['user_id']}")
        if not Product.query.get(data["product_id"]):
            abort(400, message=f"Invalid product_id: {data['product_id']}")
        if not Subscription.query.get(data["subscription_id"]):
            abort(400, message=f"Invalid subscription_id: {data['subscription_id']}")

        access_continuity.user_id = data["user_id"]
        access_continuity.product_id = data["product_id"]
        access_continuity.subscription_id = data["subscription_id"]
        access_continuity.has_access = data["has_access"]
        access_continuity.expires_at = data["expires_at"]
        db.session.commit()
        return access_continuity

    def delete(self, id):
        access_continuity = AccessContinuity.query.get(id)
        if not access_continuity:
            abort(404, message=f"Access continuity with ID {id} not found")
        db.session.delete(access_continuity)
        db.session.commit()
        return {}, 204
    
@access.route("/access/check")
class AccessCheckAPI(Resource):
    def get(self):
        user_id = request.args.get("user_id", type=int)
        product_id = request.args.get("product_id", type=int)

        if user_id is None or product_id is None:
            return {"error": "user_id and product_id are required as query parameters"}, 400

        access_entry = AccessContinuity.query.filter_by(user_id=user_id, product_id=product_id).first()

        if not access_entry:
            return {"has_access": False, "message": "No access record found"}, 404

        return {
            "has_access": access_entry.has_access,
            "expires_at": access_entry.expires_at.isoformat() if access_entry.expires_at else None
        }, 200
