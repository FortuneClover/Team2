from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Todo 생성 시 사용할 스키마
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="할 일 제목")
    description: Optional[str] = Field(None, max_length=500, description="할 일 설명")

# Todo 업데이트 시 사용할 스키마
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None

# Todo 응답 시 사용할 스키마
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # SQLAlchemy 모델을 Pydantic 모델로 변환

# 여러 Todo를 응답할 때 사용할 스키마
class TodoListResponse(BaseModel):
    todos: list[TodoResponse]
    total: int

class CheckUser(BaseModel):
    email : str
    password : str

class User(BaseModel):
    id : int
    nickname : str

class PostResponse(BaseModel):
    id : str
    title : str
    content : str
    user_id : int
    genre_id : int
    views : int

class PostListResponse(BaseModel):
    posts: list[PostResponse]
    total: int
