from app.extensions import db
from datetime import datetime

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)

    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    paid_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='paid')  # e.g., 'paid', 'refunded', 'failed'
    transaction_id = db.Column(db.String(100), unique=True)

    # Relationships
    user = db.relationship("User", back_populates="payments")
    subscription = db.relationship("Subscription", back_populates="payments")
