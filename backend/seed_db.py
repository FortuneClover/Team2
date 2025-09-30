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

# ▼▼▼ 게시물 시딩 함수 수정 ▼▼▼
def seed_posts_only(db: Session):
    """데이터베이스의 Post 테이블에 초기 테스트 데이터를 삽입합니다."""
    print("💡 Post 테이블 초기 시딩 시작...")

    if db.query(Post).count() > 0:
        print(f"  - [Post] 데이터가 이미 {db.query(Post).count()}개 존재합니다. 시딩을 건너뜁니다.")
        return

    users = db.query(User).all()
    genres = db.query(PostGenre).all()

    if not users or not genres:
        print("❌ [Post] 시딩 실패: 사용자 또는 장르 데이터가 없습니다. 먼저 시딩해주세요.")
        return
        
    posts_to_add = [
        Post(title="FastAPI 프로젝트 시작하기", content="FastAPI는 파이썬 기반의 빠르고 현대적인 웹 프레임워크입니다.", user_id=random.choice(users).id, genre_id=genres[1].id),
        Post(title="오늘의 점심 메뉴 추천", content="오늘은 날씨가 좋으니 시원한 냉면 어떠신가요?", user_id=random.choice(users).id, genre_id=genres[0].id),
        Post(title="부산 여행 후기", content="해운대 해수욕장과 광안리 야경이 정말 멋있었습니다.", user_id=random.choice(users).id, genre_id=genres[2].id),
        Post(title="요즘 듣기 좋은 플레이리스트", content="잔잔한 인디 음악부터 신나는 팝까지, 기분 전환에 좋은 노래들을 모아봤어요.", user_id=random.choice(users).id, genre_id=genres[3].id),
        Post(title="주말에 등산 다녀왔어요", content="가까운 황령산에 올랐는데, 도시 전경이 한눈에 들어와서 정말 좋았습니다.", user_id=random.choice(users).id, genre_id=genres[4].id),
        Post(title="간단한 파스타 레시피", content="토마토 소스와 마늘만 있으면 15분 만에 맛있는 파스타를 만들 수 있어요.", user_id=random.choice(users).id, genre_id=genres[5].id),
        Post(title="React 무한 스크롤 구현하기", content="IntersectionObserver API를 사용하면 스크롤 이벤트를 쉽게 감지할 수 있습니다.", user_id=random.choice(users).id, genre_id=genres[1].id),
        Post(title="새로운 카페 발견", content="전포동에 새로 생긴 카페인데, 커피 맛도 좋고 분위기도 아늑해서 추천합니다.", user_id=random.choice(users).id, genre_id=genres[0].id),
        Post(title="가을에 듣기 좋은 재즈 음악", content="쌀쌀한 날씨에 따뜻한 커피 한 잔과 함께 듣기 좋은 재즈 플레이리스트입니다.", user_id=random.choice(users).id, genre_id=genres[3].id),
        Post(title="제주도 2박 3일 여행 코스", content="동쪽 해안도로를 따라 성산일출봉과 섭지코지를 둘러보는 코스를 추천합니다.", user_id=random.choice(users).id, genre_id=genres[2].id),
        Post(title="홈 트레이닝 루틴 공유", content="매일 30분, 스쿼트와 플랭크만으로도 충분히 건강을 유지할 수 있어요.", user_id=random.choice(users).id, genre_id=genres[4].id),
        Post(title="Docker 기본 사용법", content="Docker를 사용하면 개발 환경을 컨테이너화하여 배포를 간소화할 수 있습니다.", user_id=random.choice(users).id, genre_id=genres[1].id),
        # --- 13개 추가 데이터 ---
        Post(title="퇴근 후 즐기는 맥주 한 잔", content="하루의 피로를 풀어주는 시원한 수제 맥주 맛집을 찾았어요.", user_id=random.choice(users).id, genre_id=genres[0].id),
        Post(title="SQLAlchemy ORM 기초", content="Python에서 데이터베이스를 객체처럼 다룰 수 있게 해주는 강력한 도구입니다.", user_id=random.choice(users).id, genre_id=genres[1].id),
        Post(title="강릉 당일치기 여행", content="KTX를 이용하면 서울에서 2시간 만에 강릉 바다를 볼 수 있습니다.", user_id=random.choice(users).id, genre_id=genres[2].id),
        Post(title="여름밤에 어울리는 시티팝", content="청량하고 낭만적인 분위기의 시티팝을 들으며 더위를 식혀보세요.", user_id=random.choice(users).id, genre_id=genres[3].id),
        Post(title="주말 자전거 라이딩", content="온천천을 따라 해운대까지 달리는 코스는 경치도 좋고 운동도 됩니다.", user_id=random.choice(users).id, genre_id=genres[4].id),
        Post(title="에어프라이어 활용 꿀팁", content="통삼겹 구이는 에어프라이어의 최고의 발명품입니다.", user_id=random.choice(users).id, genre_id=genres[5].id),
        Post(title="VS Code 유용한 확장 프로그램", content="Prettier, ESLint는 이제 프론트엔드 개발의 필수품이죠.", user_id=random.choice(users).id, genre_id=genres[1].id),
        Post(title="고양이 사진 대방출", content="저희 집 고양이의 귀여운 낮잠 자는 모습을 공개합니다.", user_id=random.choice(users).id, genre_id=genres[0].id),
        Post(title="혼자 보기 아까운 영화 추천", content="최근에 본 '에브리씽 에브리웨어 올 앳 원스'는 정말 인상 깊었어요.", user_id=random.choice(users).id, genre_id=genres[3].id),
        Post(title="도쿄 디즈니랜드 후기", content="놀이기구도 재미있지만, 저녁에 하는 퍼레이드가 정말 환상적입니다.", user_id=random.choice(users).id, genre_id=genres[2].id),
        Post(title="클라이밍 도전!", content="생각보다 근력을 많이 필요로 하지만, 완등했을 때의 성취감이 엄청납니다.", user_id=random.choice(users).id, genre_id=genres[4].id),
        Post(title="김치찌개 맛있게 끓이는 법", content="돼지고기를 먼저 볶다가 김치를 넣고 끓이는 것이 비법입니다.", user_id=random.choice(users).id, genre_id=genres[5].id),
        Post(title="Python 가상환경 관리", content="venv나 anaconda를 사용하면 프로젝트별로 독립된 개발 환경을 구축할 수 있습니다.", user_id=random.choice(users).id, genre_id=genres[1].id),
    ]

    db.add_all(posts_to_add)
    print(f"  - [Post] {len(posts_to_add)}개의 게시물 삽입 완료.")
    db.commit()


def seed_all_data(db: Session):
    """모든 초기 시딩 함수를 순차적으로 호출합니다."""
    print("\n--- 전체 데이터 시딩 시작 ---")
    seed_users_only(db)
    seed_genres_only(db)
    seed_posts_only(db)
    print("---------------------------\n")


if __name__ == "__main__":
    db: Session = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine) 
        seed_all_data(db)
        print("🎉 모든 시딩 작업이 성공적으로 완료되었습니다!")
    except Exception as e:
        print(f"❌ 데이터 시딩 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

