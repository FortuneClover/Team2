from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload # 👈 joinedload를 임포트합니다.
from typing import List

import models
import schemas
from database import engine, get_db, Base
import seed_db

# --- FastAPI 앱 초기화 ---
app = FastAPI(
    title="Community Board API",
    description="게시판 웹사이트를 위한 FastAPI API",
    version="1.0.0"
)

# --- CORS 미들웨어 설정 ---
# 프론트엔드 개발 서버(http://localhost:5173)에서의 요청을 허용합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FastAPI 이벤트 핸들러 (서버 시작 시) ---
@app.on_event("startup")
def on_startup():
    """서버가 시작될 때 데이터베이스 테이블을 생성하고 초기 데이터를 삽입합니다."""
    print("서버 시작: 데이터베이스 테이블을 생성합니다...")
    Base.metadata.create_all(bind=engine)
    print("테이블 생성 완료.")
    
    print("데이터 시딩을 시작합니다...")
    db = next(get_db())
    seed_db.seed_all_data(db)
    db.close()
    print("데이터 시딩 완료.")

# --- API 엔드포인트 ---

@app.get("/")
async def root():
    return {"message": "게시판 API 서버가 실행 중입니다."}

# --- 1. User (회원) API ---
@app.post("/login", response_model=schemas.UserResponse)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """사용자 로그인"""
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    return user

# --- 2. Post (게시물) API ---
@app.get("/posts", response_model=schemas.PostListResponse)
def get_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """모든 게시물 조회"""
    # Eager Loading으로 author(작성자) 정보를 함께 조회합니다.
    posts_query = db.query(models.Post).options(joinedload(models.Post.author)).order_by(models.Post.id.desc())
    
    total = posts_query.count()
    posts = posts_query.offset(skip).limit(limit).all()
    
    return {"posts": posts, "total": total}

# --- ✅ 이 부분이 추가되었습니다 ---
@app.post("/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """새로운 게시물 생성"""
    # Pydantic 모델을 SQLAlchemy 모델 인스턴스로 변환하여 DB에 저장합니다.
    db_post = models.Post(**post.dict())
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post) # DB에서 생성된 id 등의 최신 정보를 다시 불러옵니다.
    return db_post

