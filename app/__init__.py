from flask import Flask, Blueprint
from .extensions import api, db, migrate
from .resources import   freq, usr, sub, access, prod, subsplan

def create_app():
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    appBlueprint = Blueprint("app", __name__, url_prefix="/swagger")
    api.init_app(appBlueprint, title="Flask Restx Tutorial",
                 description="A simple API for a course and students",
                 validate=True
                 )
    app.register_blueprint(appBlueprint)
    
    
#the order of the namespaces matters, this is the order they appear in the swagger UI
    api.add_namespace(access)
    api.add_namespace(usr)
    api.add_namespace(freq)
    api.add_namespace(prod)
    api.add_namespace(sub)
    api.add_namespace(subsplan)



    
    return app



    # flask shell
    # from app.models import*
    # db.create_all()
    # exit()
    
    # open sqlite 
    # sqlite3 instance/db.sqlite3
    # .tables