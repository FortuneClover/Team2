from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI 인스턴스 생성
app = FastAPI(
    title="Todo API",
    description="FastAPI로 만든 Todo 관리 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "Todo API 서버가 실행 중입니다!"}

# 모든 Todo 조회
@app.get("/todos", response_model=List[schemas.TodoResponse])
def get_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """모든 Todo 항목을 조회합니다."""
    todos = db.query(models.Todo).offset(skip).limit(limit).all()
    return todos

# 특정 Todo 조회
@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """특정 ID의 Todo 항목을 조회합니다."""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first() # 리스트로 받아와지기 때문에 .first()를 사용해서 리스트에서 뺌
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id}인 Todo를 찾을 수 없습니다."
        )
    return todo

# 새로운 Todo 생성
@app.post("/todos", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """새로운 Todo 항목을 생성합니다."""
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Todo 수정
@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    """특정 ID의 Todo 항목을 수정합니다."""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id}인 Todo를 찾을 수 없습니다."
        )
    
    # 수정할 데이터만 업데이트
    update_data = todo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
    
    db.commit()
    db.refresh(todo)
    return todo

# Todo 삭제
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """특정 ID의 Todo 항목을 삭제합니다."""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id}인 Todo를 찾을 수 없습니다."
        )
    
    db.delete(todo)
    db.commit()
    return {"message": f"ID {todo_id}인 Todo가 성공적으로 삭제되었습니다."}

# 완료 상태 토글
@app.patch("/todos/{todo_id}/toggle", response_model=schemas.TodoResponse)
def toggle_todo_completion(todo_id: int, db: Session = Depends(get_db)):
    """Todo의 완료 상태를 토글합니다."""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id}인 Todo를 찾을 수 없습니다."
        )
    
    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return todo

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
