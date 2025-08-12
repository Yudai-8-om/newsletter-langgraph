from fastapi import FastAPI, Request, Depends, HTTPException
from backend.settings import settings
from backend.models.user import User
import stripe
from sqlalchemy import select
from backend.db import get_pg_async_session

webhook = FastAPI()

async def update_user_subscription(stripe_customer_id: str, subscription_id: str, subscription_status: str):
    """
    updates user subscritpion status upon webhook
    """
    async with get_pg_async_session() as session:
        stmt = select(User).where(User.stripe_customer_id == stripe_customer_id)
        result = await session.execute(stmt)
        target_user = result.scalars().one()
        target_user.stripe_subscription_id = subscription_id
        target_user.subscription_status = subscription_status
        target_user.is_subscribed = subscription_status == "active"

        await session.commit()

@webhook.post("/")
async def stripe_webhook(request: Request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        print("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")

    print("Received verified event:", event["type"])
    if event["type"] == "checkout.session.completed":
        stripe_session = event["data"]["object"] #https://docs.stripe.com/api/checkout/sessions/object
        subscription_id = stripe_session.get('subscription')
        customer_id = stripe_session.get('customer')
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        await update_user_subscription(customer_id, subscription_id,  subscription["status"])

    return {"status": "success"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("webhook:webhook", host="0.0.0.0", port=8001, reload=True)