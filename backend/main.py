from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn
# 🚨 중요: models 파일에 모든 테이블 클래스(User, Post, PostGenre 등)가 임포트되어 있어야 합니다.
import models
import schemas
from database import engine, get_db, Base # Base 임포트 추가

# 🔑 시딩 함수 임포트 (추가된 부분)
from seed_db import seed_users_only 

# 🚨 (삭제) models.Base.metadata.create_all(bind=engine) # 최상위에서 실행하는 것은 지양합니다.
# def create_tables(): # 중복된 정의 삭제


# 🔑 함수: 데이터베이스 테이블 생성 (초기화)
def create_tables():
    """모든 SQLAlchemy 모델을 기반으로 DB 테이블을 생성합니다."""
    # Base에 등록된 모든 모델을 DB 엔진에 연결하여 테이블로 만듭니다.
    print("MySQL 서버에 연결하여 테이블 생성을 시도합니다...")
    Base.metadata.create_all(bind=engine)
    print("✅ 모든 테이블 생성이 완료되었습니다!")


# FastAPI 인스턴스 생성
app = FastAPI(
    title="Posting Website API", # 프로젝트에 맞게 이름 변경
    description="게시물 웹사이트를 위한 FastAPI API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://localhost:3306", "http://localhost:8000"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


# 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "Post API 서버가 실행 중입니다!"}

@app.post("/login", response_model=schemas.User)
def login(credentials:schemas.CheckUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return user


# 모든 Post 조회
@app.get("/Posts", response_model=List[schemas.PostResponse])
def get_Posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """모든 Post 항목을 조회합니다."""
    Posts = db.query(models.Post).offset(skip).limit(limit).all()
    return Posts
    

# # 특정 Post 조회
# @app.get("/Posts/{Post_id}", response_model=schemas.PostResponse)
# def get_Post(Post_id: int, db: Session = Depends(get_db)):
#     """특정 ID의 Post 항목을 조회합니다."""
#     Post = db.query(models.Post).filter(models.Post.id == Post_id).first() # 리스트로 받아와지기 때문에 .first()를 사용해서 리스트에서 뺌
#     if not Post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"ID {Post_id}인 Post를 찾을 수 없습니다."
#         )
#     return Post

# # 새로운 Post 생성
# @app.post("/Posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
# def create_Post(Post: schemas.PostCreate, db: Session = Depends(get_db)):
#     """새로운 Post 항목을 생성합니다."""
#     db_Post = models.Post(**Post.dict())
#     db.add(db_Post)
#     db.commit()
#     db.refresh(db_Post)
#     return db_Post

# # Post 수정
# @app.put("/Posts/{Post_id}", response_model=schemas.PostResponse)
# def update_Post(
#     Post_id: int,
#     Post_update: schemas.PostUpdate,
#     db: Session = Depends(get_db)
# ):
#     """특정 ID의 Post 항목을 수정합니다."""
#     Post = db.query(models.Post).filter(models.Post.id == Post_id).first()
#     if not Post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"ID {Post_id}인 Post를 찾을 수 없습니다."
#         )
    
#     # 수정할 데이터만 업데이트
#     update_data = Post_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(Post, key, value)
    
#     db.commit()
#     db.refresh(Post)
#     return Post

# # Post 삭제
# @app.delete("/Posts/{Post_id}")
# def delete_Post(Post_id: int, db: Session = Depends(get_db)):
#     """특정 ID의 Post 항목을 삭제합니다."""
#     Post = db.query(models.Post).filter(models.Post.id == Post_id).first()
#     if not Post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"ID {Post_id}인 Post를 찾을 수 없습니다."
#         )
    
#     db.delete(Post)
#     db.commit()
#     return {"message": f"ID {Post_id}인 Post가 성공적으로 삭제되었습니다."}

# # 완료 상태 토글
# @app.patch("/Posts/{Post_id}/toggle", response_model=schemas.PostResponse)
# def toggle_Post_completion(Post_id: int, db: Session = Depends(get_db)):
#     """Post의 완료 상태를 토글합니다."""
#     Post = db.query(models.Post).filter(models.Post.id == Post_id).first()
#     if not Post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"ID {Post_id}인 Post를 찾을 수 없습니다."
#         )
    
#     Post.completed = not Post.completed
#     db.commit()
#     db.refresh(Post)
#     return Post

# 서버 실행
if __name__ == "__main__":
    # 1. 테이블 생성 함수 호출
    create_tables() 
    
    # 2. 시딩 함수 호출 (seed_db.py 실행)
    seed_users_only() # <--- 이 부분이 추가되었습니다.
    
    # 3. Uvicorn 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
