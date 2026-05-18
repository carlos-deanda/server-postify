from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.post import Post
from app.models.like import Like
from app.models.comment import Comment
from app.schemas.post import PostCreate, PostRead, PostReadDetails
from app.schemas.like import LikeRead, LikeCreate
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get('/', response_model=List[PostRead])
async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post))
    return result.scalars().all()

""" @router.get('/{post_id}', response_model=PostRead)
async def get_post_by_id(post_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return post """

@router.post('/', response_model=PostRead, status_code=201)
async def create_post(data: PostCreate, session: AsyncSession = Depends(get_session)):
    post = Post(**data.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@router.get('/{post_id}', response_model=PostReadDetails)
async def get_post_by_id(post_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    like_result = await session.execute(select(Like).where(Like.post_id == post_id))
    likes = like_result.scalars().all()

    comments_result = await session.execute(select(Comment).where(Comment.post_id == post_id))
    comments = comments_result.scalars().all()

    return PostReadDetails(
        id=post_id,
        user_id=post.user_id,
        description=post.description,
        created_at=post.created_at,
        likes=[LikeRead(**like.model_dump()) for like in likes],
        comments=[CommentRead(**comment.model_dump()) for comment in comments]
    )
    


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

@router.post('/{post_id}/likes', response_model=LikeRead, status_code=201)
async def add_like(post_id: uuid.UUID, data: LikeCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_like = await session.execute(
        select(Like).where(Like.post_id == post_id, Like.user_id == data.user_id)
    )

    if existing_like.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Like already exists")

    like = Like(user_id=data.user_id, post_id=post_id)
    session.add(like)
    await session.commit()
    await session.refresh(like)

    return LikeRead(**like.model_dump())

@router.post('/{post_id}/comments', response_model=CommentRead, status_code=201)
async def add_comment(post_id: uuid.UUID, data:CommentCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment_data = data.model_dump()
    comment_data["post_id"] = post_id
    comment = Comment(**comment_data)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return CommentRead(**comment.model_dump())

       

    

    
