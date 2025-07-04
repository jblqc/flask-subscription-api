from flask import request
from werkzeug.exceptions import NotFound
from flask_restx import Resource, Namespace, abort
from app.models.product import Product
from app.extensions import db
from app.api_models.product_models import product_model, product_input_model

prod = Namespace("Product", path="/api", description="Product management")

@prod.route("/products")
class ProductListAPI(Resource):
    # marshal_list_with is used to convert the list of courses to the Course model
    # mauunang kunin yung return results, tsaka pupunta sa marshal
    @prod.marshal_list_with(product_model)
    def get(self):
        return Product.query.all()

    @prod.expect(product_input_model)
    @prod.marshal_with(product_model)
    def post(self):
        data = request.json
        product = Product(
            name = data["name"],
            price = data["price"],
            description = data["description"],
            is_active = data["is_active"]
        )
        db.session.add(product)
        db.session.commit()
        return product, 201


@prod.route("/products/<int:id>")
class ProductAPI(Resource):
    
    @prod.marshal_with(product_model)
    def get(self, id):
        product = Product.query.get(id)
        if not product:
            abort(404, message=f"Product with ID {id} not found")
        return product

    @prod.expect(product_input_model)
    @prod.marshal_with(product_model)
    def put(self, id):
        product = Product.query.get(id)
        if not product:
            abort(404, message=f"Product with ID {id} not found")
        data = request.json
        product.name = data["name"]
        product.price = data["price"]
        product.description = data["description"]
        product.is_active = data["is_active"]
        
        db.session.commit()
        return product, 200

    def delete(self, id):
        product = Product.query.get(id)
        if not product:
            abort(404, message=f"Product with ID {id} not found")
        db.session.delete(product)
        db.session.commit()
        return {}, 204
