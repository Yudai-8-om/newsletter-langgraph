import asyncio
import asyncpg
from typing import Annotated, List
from fastapi import FastAPI, Depends, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import stripe
from backend.db import fastapi_async_session_dependency
from backend.models.newsletter import Newsletter, NewsletterResponse, NewNewsletter
from backend.models.user import User, UserEntry, UserResponse, UserSubscriptionEntry
from backend.settings import settings
from backend.auth import hash_password, create_access_token, verify_password, get_current_user, Token
from backend.tools import create_stripe_customer, create_stripe_subscription_session, update_user_subscription



app = FastAPI()

origins = [
    "https://newsletter-langgraph.vercel.app",
    "http://localhost:5173", # dev usage
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Newsletter Agent API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/register", response_model=Token)
async def register_user(new_user: UserEntry, session: AsyncSession = Depends(fastapi_async_session_dependency)):
    """Register a new user"""
    existing_user = await session.execute(select(User).where(User.email == new_user.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Log in instead."
        )
    stripe_customer = create_stripe_customer(new_user.email)
    hashed_password = hash_password(new_user.password)
    user = User(email=new_user.email, hashed_password=hashed_password, stripe_customer_id=stripe_customer.id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token}

@app.post("/login", response_model=Token)
async def login_user(user: UserEntry, session: AsyncSession = Depends(fastapi_async_session_dependency)):
    """Log in an existing user"""
    result = await session.execute(select(User).where(User.email == user.email))
    expected_user = result.scalar_one_or_none()
    if not expected_user or not verify_password(user.password, expected_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    token = create_access_token(data={"sub": str(expected_user.id)})
    return {"access_token": token}

@app.get("/me", response_model=UserResponse)
async def get_newsletters(user: User = Depends(get_current_user)):
    """Get user info"""
    return user

@app.delete("/user")
async def delete_user(user: UserEntry, session: AsyncSession = Depends(fastapi_async_session_dependency)):
    """ Detele user"""
    result = await session.execute(select(User).where(User.email == user.email))
    expected_user = result.scalar_one_or_none()
    if not expected_user or not verify_password(user.password, expected_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid request"
        )

    stripe.api_key = settings.STRIPE_SECRET_KEY
    if expected_user.stripe_subscription_id:
        try:
            stripe.Subscription.cancel(expected_user.stripe_subscription_id)
        except stripe.error.InvalidRequestError as e:
            if "No such subscription" in str(e):
                pass
            else:
                raise
    if expected_user.stripe_customer_id:
        try:
            stripe.Customer.delete(expected_user.stripe_customer_id)
        except stripe.error.InvalidRequestError as e:
            if "No such customer" in str(e):
                pass
            else:
                raise

    await session.execute(delete(User).where(User.email == user.email))
    await session.commit()
    return {"detail": "User deleted successfully"}


@app.get("/newsletters", response_model=List[NewsletterResponse])
async def get_newsletters(session: AsyncSession = Depends(fastapi_async_session_dependency), user: User = Depends(get_current_user)):
    """Get last 7 days newsletters"""
    result = await session.execute(select(Newsletter).order_by(Newsletter.created_at.desc()).limit(7))
    newsletters = result.scalars().all()
    if not newsletters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No newsletters found"
        )
    return newsletters

@app.get("/newsletters/{newsletter_id}", response_model=NewsletterResponse)
async def get_newsletter(newsletter_id: int, session: AsyncSession = Depends(fastapi_async_session_dependency)):
    """Get a specific newsletter by ID"""
    result = await session.execute(select(Newsletter).where(Newsletter.id == newsletter_id))
    newsletter = result.scalar_one_or_none()
    if not newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Newsletter with id {newsletter_id} not found"
        )
    return newsletter

@app.post("/newsletters", response_model=NewsletterResponse, status_code=status.HTTP_201_CREATED)
async def create_newsletter(newsletter_data: NewNewsletter, session: AsyncSession = Depends(fastapi_async_session_dependency)):
    """Create a new newsletter"""
    new_newsletter = Newsletter(
        title=newsletter_data.title,
        content=newsletter_data.content
    )
    
    session.add(new_newsletter)
    await session.commit()
    await session.refresh(new_newsletter)
    
    return new_newsletter

@app.post("/subscription")
async def activate_subscription(entry: UserSubscriptionEntry, user: User = Depends(get_current_user)):
    try: 
        session = create_stripe_subscription_session(user.stripe_customer_id)
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stripe-webhook")
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
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)


