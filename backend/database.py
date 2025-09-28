from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 데이터베이스 URL
# 형식: mysql+pymysql://username:password@host:port/database_name
DATABASE_URL = "mysql+pymysql://root:doitmysql@localhost:3306/todoapp"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL 쿼리 로그 출력 (개발 시에만 True)
    pool_pre_ping=True,  # 연결 확인
    pool_recycle=300,  # 연결 재활용 시간
)

# 세션 로컬 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
