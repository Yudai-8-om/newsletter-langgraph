from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from .base import Base
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr



class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_subscribed: Mapped[bool] = mapped_column(default=False)
    stripe_customer_id: Mapped[str | None] = mapped_column(nullable=True)
    stripe_subscription_id: Mapped[str | None] = mapped_column(nullable=True)
    subscription_status: Mapped[str | None] = mapped_column(nullable=True)
    subscription_end: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )
    
class UserEntry(BaseModel):
    """
    Schema for creating a new user.
    """
    email: EmailStr
    password: str

class UserSubscriptionEntry(BaseModel):
    """
    Schema for subscription management.
    """
    subscription: str

class UserResponse(BaseModel):
    """
    Schema for user response.
    """
    email: EmailStr
    is_subscribed: bool
    
    model_config = ConfigDict(
        from_attributes=True)