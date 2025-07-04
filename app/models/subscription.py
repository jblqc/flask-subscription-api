from app.extensions import db

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    subscription_plan_id = db.Column(db.Integer, db.ForeignKey("subscription_plan.id"), nullable=False)

    status = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    renewal_date = db.Column(db.DateTime, nullable=True)
    auto_renew = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship("User", back_populates="subscriptions")
    subscription_plan = db.relationship("SubscriptionPlan", back_populates="subscriptions")
    access_continuity = db.relationship("AccessContinuity", uselist=False, back_populates="subscription", cascade="all, delete-orphan")
