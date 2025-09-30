from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# ==================================================================
# User (회원) 관련 스키마
# ==================================================================

# --- 로그인 요청 시 사용할 스키마 ---
class UserLogin(BaseModel):
    email: str
    password: str

# --- 응답 시 클라이언트에게 전달할 사용자 정보 스키마 ---
#    (비밀번호 등 민감한 정보는 제외)
class UserResponse(BaseModel):
    id: int
    nickname: str
    email: str

    class Config:
        from_attributes = True # SQLAlchemy 모델을 Pydantic 모델로 변환

# ==================================================================
# Post (게시물) 관련 스키마
# ==================================================================

# --- 게시물 응답 시 사용할 스키마 ---
#    - author 필드에 위에서 정의한 UserResponse 스키마를 사용하여
#      작성자 정보를 객체 형태로 포함시킵니다.
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    views: int
    created_at: datetime
    author: UserResponse # 👈 이 부분이 핵심적인 변경사항입니다.

    class Config:
        from_attributes = True

# --- 여러 게시물을 응답할 때 사용할 스키마 ---
class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total: int
