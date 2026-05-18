from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get('/', response_model=List[PostRead])
async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post))
    return result.scalars().all()

@router.get('/{post_id}', response_model=PostRead)
async def get_post_by_id(post_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return post

@router.post('/', response_model=PostRead, status_code=201)
async def create_post(data: PostCreate, session: AsyncSession = Depends(get_session)):
    # Corregido el "comit" que tenías
    post = Post(**data.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@router.put('/{post_id}', response_model=PostRead)
async def update_post(post_id: uuid.UUID, data: PostCreate, session: AsyncSession = Depends(get_session)):
    db_post = await session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    post_data = data.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(db_post, key, value)
    
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post

@router.delete('/{post_id}', status_code=204)
async def delete_post(post_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    await session.delete(post)
    await session.commit()
    return None
