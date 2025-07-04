from app.extensions import db

class AccessContinuity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey("subscription.id"), nullable=False)

    has_access = db.Column(db.Boolean, nullable=False, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    # Relationships
    subscription = db.relationship("Subscription", back_populates="access_continuity", uselist=False)
    user = db.relationship("User", back_populates="access_entries")
    product = db.relationship("Product", back_populates="access_continuity")
