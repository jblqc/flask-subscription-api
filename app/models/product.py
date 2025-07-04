from app.extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    subscription_plan = db.relationship("SubscriptionPlan", back_populates="product", cascade="all, delete-orphan")
    access_continuity = db.relationship("AccessContinuity", back_populates="product", cascade="all, delete-orphan")

