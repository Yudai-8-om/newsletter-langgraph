import asyncio
import asyncpg
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db import get_pg_async_session
from backend.models import Newsletter, NewsletterResponse, NewNewsletter
from typing import List
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Newsletter Agent API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/newsletters", response_model=List[NewsletterResponse])
async def get_newsletters(session: AsyncSession = Depends(get_pg_async_session)):
    """Get last 7 days newsletters"""
    result = await session.execute(select(Newsletter).order_by(Newsletter.created_at.desc()).limit(7))
    newsletters = result.scalars().all()
    return newsletters

@app.get("/newsletters/{newsletter_id}", response_model=NewsletterResponse)
async def get_newsletter(newsletter_id: int, session: AsyncSession = Depends(get_pg_async_session)):
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
async def create_newsletter(newsletter_data: NewNewsletter, session: AsyncSession = Depends(get_pg_async_session)):
    """Create a new newsletter"""
    new_newsletter = Newsletter(
        title=newsletter_data.title,
        content=newsletter_data.content
    )
    
    session.add(new_newsletter)
    await session.commit()
    await session.refresh(new_newsletter)
    
    return new_newsletter


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


