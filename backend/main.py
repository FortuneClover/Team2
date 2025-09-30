from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload # 👈 joinedload 임포트
from typing import List
import uvicorn

# --- 프로젝트 모듈 임포트 ---
import models
import schemas
from database import engine, get_db, Base
import seed_db # 시딩 함수 임포트

# FastAPI 인스턴스 생성
app = FastAPI(
    title="Posting Website API",
    description="게시물 웹사이트를 위한 FastAPI API",
    version="1.0.0"
)

# ==================================================================
# 💡 애플리케이션 시작 시 실행될 이벤트 핸들러
# ==================================================================
@app.on_event("startup")
def on_startup():
    """
    애플리케이션이 시작될 때 한 번만 실행됩니다.
    데이터베이스 테이블을 생성하고 초기 데이터를 시딩합니다.
    --reload 모드에서도 한 번만 실행되어 안전합니다.
    """
    print("🚀 애플리케이션 시작...")
    
    # 1. 테이블 생성
    print("🔧 데이터베이스 테이블 생성을 시작합니다...")
    Base.metadata.create_all(bind=engine)
    print("✅ 모든 테이블이 성공적으로 생성되었습니다.")

    # 2. 데이터 시딩
    print("🌱 초기 데이터 시딩을 시작합니다...")
    db = next(get_db()) # 시딩을 위한 일회용 DB 세션 생성
    try:
        # seed_db.py에 정의된 통합 시딩 함수를 호출합니다.
        seed_db.seed_all_data(db)
        print("✅ 모든 데이터 시딩이 성공적으로 완료되었습니다.")
    finally:
        db.close() # 세션 닫기
    
    print("🎉 서버가 성공적으로 시작되었습니다!")

# ==================================================================
# CORS 설정
# ==================================================================
app.add_middleware(
    CORSMiddleware,
    # 프론트엔드 개발 서버 주소만 허용하는 것이 좋습니다.
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================================
# API 라우트 (엔드포인트)
# ==================================================================

@app.get("/")
async def root():
    return {"message": "Post API 서버가 실행 중입니다!"}

# --- 로그인 API ---
@app.post("/login", response_model=schemas.UserResponse) # 👈 응답 모델 수정: User -> UserResponse
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)): # 👈 입력 모델 수정: CheckUser -> UserLogin
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    return user

# --- 모든 게시물 조회 API ---
@app.get("/posts", response_model=schemas.PostListResponse) # 👈 경로 수정 및 응답 모델 변경
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    모든 게시물을 조회합니다.
    작성자(author) 정보를 함께 로드하여 반환합니다.
    """
    # 쿼리: posts 테이블과 연관된 author(users 테이블)를 함께 조회 (Eager Loading)
    posts_query = db.query(models.Post).options(joinedload(models.Post.author))
    
    total = posts_query.count()
    posts = posts_query.offset(skip).limit(limit).all()
    
    # PostListResponse 스키마에 맞게 응답 데이터를 구성합니다.
    return {"posts": posts, "total": total}

# ==================================================================
# (참고) uvicorn 직접 실행 (터미널에서 실행하는 것을 권장)
# ==================================================================
if __name__ == "__main__":
    # 터미널에서 'uvicorn main:app --reload' 명령어로 실행하는 것이 일반적입니다.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
