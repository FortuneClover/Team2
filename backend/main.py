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
    return {"message": "Todo API 서버가 실행 중입니다!"}

@app.post("/login", response_model=schemas.CheckUser)
def check_user(
    user_id : str,
    password : str,
    db : Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == user_id).first()
    return user


# # 모든 Todo 조회
# @app.get("/todos", response_model=List[schemas.TodoResponse])
# def get_todos(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db)
# ):
#     """모든 Todo 항목을 조회합니다."""
#     todos = db.query(models.Todo).offset(skip).limit(limit).all()
#     return todos

# # 특정 Todo 조회
# @app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
# def get_todo(todo_id: int, db: Session = Depends(get_db)):
#     """특정 ID의 Todo 항목을 조회합니다."""
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first() # 리스트로 받아와지기 때문에 .first()를 사용해서 리스트에서 뺌
#     if not todo:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"ID {todo_id}인 Todo를 찾을 수 없습니다."
#         )
#     return todo

# # 새로운 Todo 생성
# @app.post("/todos", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
# def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
#     """새로운 Todo 항목을 생성합니다."""
#     db_todo = models.Todo(**todo.dict())
#     db.add(db_todo)
#     db.commit()
#     db.refresh(db_todo)
#     return db_todo

# # Todo 수정
# @app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
# def update_todo(
#     todo_id: int,
#     todo_update: schemas.TodoUpdate,
#     db: Session = Depends(get_db)
# ):
#     """특정 ID의 Todo 항목을 수정합니다."""
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     if not todo:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"ID {todo_id}인 Todo를 찾을 수 없습니다."
#         )
    
#     # 수정할 데이터만 업데이트
#     update_data = todo_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(todo, key, value)
    
#     db.commit()
#     db.refresh(todo)
#     return todo

# # Todo 삭제
# @app.delete("/todos/{todo_id}")
# def delete_todo(todo_id: int, db: Session = Depends(get_db)):
#     """특정 ID의 Todo 항목을 삭제합니다."""
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     if not todo:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"ID {todo_id}인 Todo를 찾을 수 없습니다."
#         )
    
#     db.delete(todo)
#     db.commit()
#     return {"message": f"ID {todo_id}인 Todo가 성공적으로 삭제되었습니다."}

# # 완료 상태 토글
# @app.patch("/todos/{todo_id}/toggle", response_model=schemas.TodoResponse)
# def toggle_todo_completion(todo_id: int, db: Session = Depends(get_db)):
#     """Todo의 완료 상태를 토글합니다."""
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     if not todo:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"ID {todo_id}인 Todo를 찾을 수 없습니다."
#         )
    
#     todo.completed = not todo.completed
#     db.commit()
#     db.refresh(todo)
#     return todo

# 서버 실행
if __name__ == "__main__":
    # 1. 테이블 생성 함수 호출
    create_tables() 
    
    # 2. 시딩 함수 호출 (seed_db.py 실행)
    seed_users_only() # <--- 이 부분이 추가되었습니다.
    
    # 3. Uvicorn 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
