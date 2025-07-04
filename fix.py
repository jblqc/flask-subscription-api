from app.extensions import db
from app.models.subscription_plan import SubscriptionPlan

plans = SubscriptionPlan.query.filter(SubscriptionPlan.plan_price == None).all()
for plan in plans:
    plan.plan_price = 0.0
db.session.commit()
