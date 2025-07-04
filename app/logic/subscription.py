from datetime import datetime, timedelta
from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan
from app.models.access_continuity import AccessContinuity
from app.extensions import db

def renew_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return {"error": f"Subscription with ID {subscription_id} not found"}, 404

    plan = SubscriptionPlan.query.get(subscription.subscription_plan_id)
    if not plan or not plan.frequency_option:
        return {"error": f"Invalid or missing plan/frequency for subscription ID {subscription_id}"}, 400

    # STEP 1 — Simulate Payment First
    plan_price = plan.plan_price or 0.0
    payment = Payment(
        user_id=subscription.user_id,
        subscription_id=subscription.id,
        payment_method="credit_card",  # or pull from config/input
        transaction_id=f"renewal_{datetime.utcnow().timestamp()}",
        amount=plan_price,
        status="success"  # simulated
    )
    db.session.add(payment)

    if payment.status != "success":
        db.session.rollback()
        return {"error": "Payment failed. Subscription not renewed."}, 402

    # STEP 2 — Proceed with renewal
    now = datetime.utcnow()
    duration = timedelta(days=plan.frequency_option.duration_days)
    new_end_date = now + duration

    subscription.end_date = new_end_date
    subscription.renewal_date = now
    subscription.status = "subscribed"

    access = AccessContinuity.query.filter_by(subscription_id=subscription_id).first()
    if access:
        access.expires_at = new_end_date
        access.has_access = True

    db.session.commit()

    return {
        "message": "Subscription successfully renewed",
        "subscription_id": subscription_id,
        "new_end_date": new_end_date.isoformat(),
        "renewal_date": now.isoformat(),
        "payment_id": payment.id
    }

def cancel_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return {"error": f"Subscription with ID {subscription_id} not found"}, 404

    subscription.status = "unsubscribed"
    subscription.auto_renew = False

    access = AccessContinuity.query.filter_by(subscription_id=subscription_id).first()
    if access:
        access.has_access = False

    db.session.commit()

    return {"message": "Subscription successfully canceled", "subscription_id": subscription_id}


def expire_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return {"error": f"Subscription with ID {subscription_id} not found"}, 404

    now = datetime.utcnow()
    subscription.status = "expired"
    subscription.end_date = now

    access = AccessContinuity.query.filter_by(subscription_id=subscription_id).first()
    if access:
        access.expires_at = now
        access.has_access = False

    db.session.commit()

    return {"message": "Subscription manually expired", "subscription_id": subscription_id, "expired_at": now.isoformat()}
