from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func
from database import Base # database.py에서 정의된 Base를 사용

# ----------------------------------------------------
# 1. 회원정보 (User) 테이블 정의
# ----------------------------------------------------
class User(Base):
    __tablename__ = "users" # 회원정보 테이블

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="회원id")
    email = Column(String(100), unique=True, nullable=False, index=True)
    nickname = Column(String(50), unique=True, nullable=False, comment="닉네임")
    password = Column(String(255), nullable=False, comment="비밀번호") 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="가입일")

    # 관계: User는 여러 Post를 가질 수 있습니다.
    posts = relationship("Post", back_populates="author")
    # 관계: User는 여러 Comment를 작성할 수 있습니다.
    comments = relationship("Comment", back_populates="author")

# ----------------------------------------------------
# 2. 게시물 장르 (PostGenre) 테이블 정의
# ----------------------------------------------------
class PostGenre(Base):
    __tablename__ = "post_genres" # 게시물장르 테이블

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="장르id")
    name = Column(String(50), unique=True, nullable=False, comment="장르")

    # 관계: PostGenre는 여러 Post를 가질 수 있습니다.
    posts = relationship("Post", back_populates="genre")

# ----------------------------------------------------
# 3. 게시물 (Post) 테이블 정의
# ----------------------------------------------------
class Post(Base):
    __tablename__ = "posts" # 게시물 테이블

    # 기본 키 및 내용 필드
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="게시물id")
    title = Column(String(200), nullable=False, index=True, comment="제목")
    content = Column(Text, nullable=False, comment="본문내용") 

    # 🔑 외래 키 (FK) 설정: 작성자 및 장르
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="회원id")
    genre_id = Column(Integer, ForeignKey("post_genres.id"), nullable=False, comment="장르id")

    # 메타 데이터 필드
    views = Column(Integer, default=0, nullable=False, comment="조회수")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="작성시간")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="수정시간")

    # 관계 정의 (Python 객체 접근용)
    author = relationship("User", back_populates="posts")
    genre = relationship("PostGenre", back_populates="posts")
    # 관계: Post는 여러 Comment를 가질 수 있습니다.
    comments = relationship("Comment", back_populates="post")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', author_id={self.user_id})>"
    
# ----------------------------------------------------
# 4. 댓글 (Comment) 테이블 정의 (신규 추가)
# ----------------------------------------------------
class Comment(Base):
    __tablename__ = "comments" # 댓글 테이블

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="댓글id")
    content = Column(Text, nullable=False, comment="댓글 내용")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="작성시간")
    
    # 🔑 외래 키 (FK) 설정: 게시물 및 작성자
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, comment="게시물id")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="회원id")
    
    # 관계 정의
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
