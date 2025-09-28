from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func # sql의 함수를 사용가능, func.()
from database import Base # database.py

class Todo(Base): # 의존성 주입 (depends)
    __tablename__ = "todos"

    # table 필드 정의
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed})>"