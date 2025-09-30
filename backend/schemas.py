from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# ==================================================================
# User (회원) 관련 스키마
# ==================================================================

# --- 로그인 요청 시 사용할 스키마 ---
class UserLogin(BaseModel):
    """로그인 시 이메일과 비밀번호를 받기 위한 모델입니다."""
    email: str
    password: str

# --- 응답 시 클라이언트에게 전달할 사용자 정보 스키마 ---
class UserResponse(BaseModel):
    """비밀번호 등 민감 정보를 제외하고 응답할 때 사용하는 사용자 모델입니다."""
    id: int
    nickname: str
    email: str

    class Config:
        from_attributes = True # SQLAlchemy 모델을 Pydantic 모델로 자동 변환합니다.

# ==================================================================
# Genre (장르) 관련 스키마 (신규 추가)
# ==================================================================
class GenreResponse(BaseModel):
    """장르 정보를 응답으로 보낼 때의 형식입니다."""
    id: int
    name: str

    class Config:
        from_attributes = True

class GenreListResponse(BaseModel):
    """장르 목록 전체를 응답으로 보낼 때의 형식입니다."""
    genres: List[GenreResponse]
    total: int

# ==================================================================
# Post (게시물) 관련 스키마
# ==================================================================

# --- 게시물의 기본 필드를 정의 (코드 중복 방지용) ---
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="게시물 제목")
    content: str = Field(..., min_length=1, description="게시물 내용")

# --- 새로운 게시물을 생성할 때 사용할 스키마 ---
class PostCreate(PostBase):
    """
    프론트엔드에서 새로운 게시물을 만들 때 보내는 데이터의 형식입니다.
    user_id와 genre_id를 반드시 포함해야 합니다.
    """
    user_id: int
    genre_id: int

# --- 게시물 응답 시 사용할 스키마 ---
class PostResponse(PostBase):
    """
    클라이언트에게 게시물 정보를 응답으로 보낼 때의 형식입니다.
    작성자 정보(author)가 객체 형태로 포함됩니다.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    views: int
    author: UserResponse

    class Config:
        from_attributes = True

# --- 여러 게시물을 응답할 때 사용할 스-키마 ---
class PostListResponse(BaseModel):
    """게시물 목록 전체를 응답으로 보낼 때의 형식입니다."""
    posts: List[PostResponse]
    total: int

