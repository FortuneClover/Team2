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

# ... (CORS 설정 및 엔드포인트 코드는 그대로 유지) ...

# 루트 엔드포인트
@app.get("/")
async def root():
    # 이제 테이블 생성이 분리되었으므로, 서버가 실행 중임을 알리는 메시지로 충분합니다.
    return {"message": "게시물 API 서버가 실행 중입니다!"}

# ... (get_todos, create_todo, update_todo 등의 CRUD 엔드포인트 유지) ...

# -------------------------------------------------------------
# 서버 실행
if __name__ == "__main__":
    # 1. 테이블 생성 함수 호출
    create_tables() 
    
    # 2. 시딩 함수 호출 (seed_db.py 실행)
    seed_users_only() # <--- 이 부분이 추가되었습니다.
    
    # 3. Uvicorn 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
