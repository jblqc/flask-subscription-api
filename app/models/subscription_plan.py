from app.extensions import db

class SubscriptionPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    frequency_option_id = db.Column(db.Integer, db.ForeignKey("frequency_option.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    plan_price = db.Column(db.Float, nullable=False, default=0.0)
    # Relationships
    product = db.relationship("Product", back_populates="subscription_plan")
    frequency_option = db.relationship("FrequencyOption", back_populates="subscription_plans")
    subscriptions = db.relationship("Subscription", back_populates="subscription_plan", cascade="all, delete-orphan")
