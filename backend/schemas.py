from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# ==================================================================
# User (회원) 관련 스키마
# ==================================================================
class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    nickname: str
    email: str
    class Config: from_attributes = True

# ==================================================================
# Genre (장르) 관련 스키마
# ==================================================================
class GenreResponse(BaseModel):
    id: int
    name: str
    class Config: from_attributes = True

class GenreListResponse(BaseModel):
    genres: List[GenreResponse]
    total: int

# ==================================================================
# Post (게시물) 관련 스키마
# ==================================================================
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)

class PostCreate(PostBase):
    user_id: int
    genre_id: int

class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    views: int
    author: UserResponse
    genre: GenreResponse  # 👈 이 필드가 추가되었습니다.

    class Config:
        from_attributes = True

class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total: int

