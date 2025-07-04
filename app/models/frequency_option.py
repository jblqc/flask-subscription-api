from app.extensions import db
"""
    First is to define the models for the db.

    This file contains the models for the database. this are still python objects
    In here, you can define the structure of the database, and the relationships.


    """

class FrequencyOption(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)

    frequency = db.Column(db.String(50), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    
    #Relationships
    subscription_plans = db.relationship("SubscriptionPlan", back_populates="frequency_option")

    

