from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.user import User
from app.models.post import Post
from app.schemas.user import UserCreate, UserRead
from app.schemas.post import PostRead


router = APIRouter(prefix="/users", tags=["users"])

@router.get('/', response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

@router.get('/{user_id}', response_model=UserRead)
async def get_user_by_id(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post('/', response_model=UserRead, status_code=201)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(**data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.put('/{user_id}', response_model=UserRead)
async def update_user(user_id: uuid.UUID, data: UserCreate, session: AsyncSession = Depends(get_session)):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_data = data.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@router.delete('/{user_id}', status_code=204)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    await session.delete(user)
    await session.commit()
    return None

@router.get('/{userId}/posts', response_model=List[PostRead], status_code=200)
async def get_posts_by_user(userId: uuid.UUID, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Post).where(Post.user_id == userId))
    return res.scalars().all()