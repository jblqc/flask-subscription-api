from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)

        # Relationships
    #casecade="all, delete-orphan" means that if the user is deleted,
    # all the subscriptions and access_entries will be deleted
    subscriptions = db.relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    access_entries = db.relationship("AccessContinuity", back_populates="user", cascade="all, delete-orphan")