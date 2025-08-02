from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from .base import Base
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Newsletter(Base):
    __tablename__ = 'newsletters'
    id: Mapped[int]= mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class NewNewsletter(BaseModel):
    title: str
    content: str

class NewsletterResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True)