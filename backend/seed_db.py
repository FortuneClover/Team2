from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from models import User

# 테이블이 없다면 생성 (User 테이블 포함 모든 모델 생성)
Base.metadata.create_all(bind=engine)

def seed_users_only():
    """데이터베이스의 User 테이블에만 초기 테스트 데이터를 삽입합니다."""
    db: Session = SessionLocal()
    
    try:
        print("💡 User 테이블 초기 시딩 시작...")

        # 1. 테스트 사용자 데이터 삽입 (Users)
        
        # User 데이터가 하나라도 있으면 작업을 건너뜁니다.
        if db.query(User).count() > 0:
            print(f"  - [User] 데이터가 이미 {db.query(User).count()}개 존재합니다. 시딩을 건너뜁니다.")
            return

        # 삽입할 사용자 목록
        users_to_add = [
            User(
                email="mz@naver.com", 
                nickname="mz", 
                password="mz" # 실제로는 암호화된 값
            ),
            User(
                email="tjdgus01@naver.com", 
                nickname="쵸쵸_님", 
                password="chocho"
            ),
            User(
                email="seungmo975", 
                nickname="손승모", 
                password="tmdah5589@"
            )
        ]
            
        db.add_all(users_to_add)
        db.commit()
        print(f"  - [User] {len(users_to_add)}명의 사용자 삽입 완료.")
        
        print("🎉 User 테이블 시딩 작업이 완료되었습니다!")

    except Exception as e:
        db.rollback()
        print(f"❌ 데이터 시딩 중 오류 발생: {e}")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_users_only()
