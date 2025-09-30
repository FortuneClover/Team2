from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
# 필요한 모델 모두 임포트
from models import User, PostGenre, Post
import random

def seed_users_only(db: Session):
    """데이터베이스의 User 테이블에만 초기 테스트 데이터를 삽입합니다."""
    print("💡 User 테이블 초기 시딩 시작...")
    if db.query(User).count() > 0:
        print(f"  - [User] 데이터가 이미 {db.query(User).count()}개 존재합니다. 시딩을 건너뜁니다.")
        return

    users_to_add = [
        User(email="mz@naver.com", nickname="mz", password="mz"),
        User(email="tjdgus01@naver.com", nickname="쵸쵸_님", password="chocho"),
        User(email="seungmo975@naver.com", nickname="손승모", password="tmdah5589@")
    ]
    db.add_all(users_to_add)
    print(f"  - [User] {len(users_to_add)}명의 사용자 삽입 완료.")
    db.commit()

def seed_genres_only(db: Session):
    """데이터베이스의 PostGenre 테이블에만 초기 테스트 데이터를 삽입합니다."""
    print("💡 PostGenre 테이블 초기 시딩 시작...")
    if db.query(PostGenre).count() > 0:
        print(f"  - [PostGenre] 데이터가 이미 {db.query(PostGenre).count()}개 존재합니다. 시딩을 건너뜁니다.")
        return

    genres_to_add = [
        PostGenre(name="일상"), PostGenre(name="기술"), PostGenre(name="여행"),
        PostGenre(name="음악"), PostGenre(name="스포츠"), PostGenre(name="요리")
    ]
    db.add_all(genres_to_add)
    print(f"  - [PostGenre] {len(genres_to_add)}개의 장르 삽입 완료.")
    db.commit()

# ▼▼▼ 게시물 시딩 함수 추가 ▼▼▼
def seed_posts_only(db: Session):
    """데이터베이스의 Post 테이블에 초기 테스트 데이터를 삽입합니다."""
    print("💡 Post 테이블 초기 시딩 시작...")

    # Post 데이터가 이미 있으면 작업을 건너뜁니다.
    if db.query(Post).count() > 0:
        print(f"  - [Post] 데이터가 이미 {db.query(Post).count()}개 존재합니다. 시딩을 건너뜁니다.")
        return

    # 게시물을 작성하려면 User와 Genre 데이터가 먼저 필요합니다.
    users = db.query(User).all()
    genres = db.query(PostGenre).all()

    if not users or not genres:
        print("❌ [Post] 시딩 실패: 사용자 또는 장르 데이터가 없습니다. 먼저 시딩해주세요.")
        return
        
    posts_to_add = [
        Post(
            title="FastAPI 프로젝트 시작하기", 
            content="FastAPI는 파이썬 기반의 빠르고 현대적인 웹 프레임워크입니다. Pydantic을 이용한 타입 힌팅이 강력한 장점이죠.",
            user_id=random.choice(users).id,
            genre_id=genres[1].id # '기술' 장르
        ),
        Post(
            title="오늘의 점심 메뉴 추천", 
            content="오늘은 날씨가 좋으니 시원한 냉면 어떠신가요? 맛있는 점심 드세요!",
            user_id=random.choice(users).id,
            genre_id=genres[0].id # '일상' 장르
        ),
        Post(
            title="부산 여행 후기", 
            content="해운대 해수욕장과 광안리 야경이 정말 멋있었습니다. 다음에는 태종대에도 가보고 싶네요.",
            user_id=random.choice(users).id,
            genre_id=genres[2].id # '여행' 장르
        ),
        Post(
            title="요즘 듣기 좋은 플레이리스트", 
            content="잔잔한 인디 음악부터 신나는 팝까지, 기분 전환에 좋은 노래들을 모아봤어요.",
            user_id=random.choice(users).id,
            genre_id=genres[3].id # '음악' 장르
        )
    ]

    db.add_all(posts_to_add)
    print(f"  - [Post] {len(posts_to_add)}개의 게시물 삽입 완료.")
    db.commit()


def seed_all_data(db: Session):
    """모든 초기 시딩 함수를 순차적으로 호출합니다."""
    print("\n--- 전체 데이터 시딩 시작 ---")
    # 1. User 시딩 실행
    seed_users_only(db)
    # 2. Genre 시딩 실행
    seed_genres_only(db)
    # 3. Post 시딩 실행 (추가)
    seed_posts_only(db)
    print("---------------------------\n")


if __name__ == "__main__":
    # 데이터베이스 세션 생성
    db: Session = SessionLocal()
    
    try:
        # 모든 테이블 생성 (이미 존재하면 아무 일도 일어나지 않음)
        Base.metadata.create_all(bind=engine) 
        
        # 통합 시딩 함수 호출
        seed_all_data(db)

        print("🎉 모든 시딩 작업이 성공적으로 완료되었습니다!")

    except Exception as e:
        print(f"❌ 데이터 시딩 중 오류 발생: {e}")
        db.rollback() # 오류 발생 시 롤백
        
    finally:
        db.close() # 작업 완료 후 세션 종료
