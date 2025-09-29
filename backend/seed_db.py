from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
# 🚨 참고: Base.metadata.create_all()은 main.py의 startup 이벤트에서 처리하는 것을 권장합니다.
# seed_db.py에서는 import 시 실행되지 않도록 주의합니다.
import models
# 필요한 모델 모두 임포트
from models import User, PostGenre

# [기존: 제거 또는 주석 처리 권장] Base.metadata.create_all(bind=engine) 

def seed_users_only(db: Session):
    """데이터베이스의 User 테이블에만 초기 테스트 데이터를 삽입합니다."""
    
    print("💡 User 테이블 초기 시딩 시작...")

    # User 데이터가 하나라도 있으면 작업을 건너뜜
    if db.query(User).count() > 0:
        print(f"  - [User] 데이터가 이미 {db.query(User).count()}개 존재합니다. 시딩을 건너뜁니다.")
        return

    # 삽입할 사용자 목록
    users_to_add = [
        User(email="mz@naver.com", nickname="mz", password="mz"),
        User(email="tjdgus01@naver.com", nickname="쵸쵸_님", password="chocho"),
        User(email="seungmo975@naver.com", nickname="손승모", password="tmdah5589@")
    ]
        
    db.add_all(users_to_add)
    print(f"  - [User] {len(users_to_add)}명의 사용자 삽입 완료.")
    db.commit()
    
def seed_genres_only(db: Session):
    """데이터베이스의 PostGenre 테이블에만 초기 테스트 데이터를 삽입합니다."""
    
    print("💡 PostGenre 테이블 초기 시딩 시작...")

    # PostGenre 데이터가 하나라도 있으면 작업을 건너뜜
    if db.query(PostGenre).count() > 0:
        print(f"  - [PostGenre] 데이터가 이미 {db.query(PostGenre).count()}개 존재합니다. 시딩을 건너뜁니다.")
        return

    # 삽입할 장르 목록
    genres_to_add = [
        PostGenre(name="일상"),
        PostGenre(name="기술"),
        PostGenre(name="여행"),
        PostGenre(name="음악"),
        PostGenre(name="스포츠"),
        PostGenre(name="요리")
    ]
        
    db.add_all(genres_to_add)
    print(f"  - [PostGenre] {len(genres_to_add)}개의 장르 삽입 완료.")
    db.commit()

# --- ✅ 통합 시딩 함수 추가 ---
def seed_all_data(db: Session):
    """모든 초기 시딩 함수(User, Genre)를 순차적으로 호출합니다."""
    
    # 1. User 시딩 실행
    seed_users_only(db)
    
    # 2. Genre 시딩 실행
    seed_genres_only(db)
    
    print("✨ 모든 초기 데이터 시딩 함수 호출 완료.")


# --- 메인 실행 블록 (통합 함수를 사용하도록 수정) ---
if __name__ == "__main__":
    db: Session = SessionLocal()
    
    try:
        # 🚨 참고: 이 부분이 seed_db.py 최상단에 있다면 제거해야 합니다.
        Base.metadata.create_all(bind=engine) 
        
        # 통합 함수 호출
        seed_all_data(db)

        # 모든 변경사항을 한 번에 커밋
        db.commit()
        print("🎉 모든 시딩 작업이 완료되었습니다!")

    except Exception as e:
        db.rollback()
        print(f"❌ 데이터 시딩 중 오류 발생: {e}")
        
    finally:
        db.close()