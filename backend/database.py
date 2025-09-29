from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 데이터베이스 URL (pymysql 드라이버 명시)
DATABASE_URL = "mysql+pymysql://root:tmdah5589%40@localhost:3306/posting_website_db"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
)

# 세션 로컬 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

# 데이터베이스 세션 의존성 (FastAPI 등에서 사용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()