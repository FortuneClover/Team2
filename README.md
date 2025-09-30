# Team2

1. todo앱을 기반으로 질문을 하는 형식
2. 로그인, 게시물 접근 페이지, 게시물 리스트 페이지(궁극적으로는 3가지의 페이지, 프로토 타입은 2개[로그인, todoapp]
3. frontend : 디자인(김성현), backend(손승모), jsx(김민준)

ppt link
https://www.canva.com/design/DAG0b3XLHkA/2YJboctumxTS4rGL8lyAQg/edit?utm_content=DAG0b3XLHkA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Team2/
├── backend/
│   ├── database.py          # 데이터베이스 연결
│   ├── models.py            # SQLAlchemy 모델
│   ├── schemas.py           # Pydantic 스키마
│   ├── main.py              # FastAPI 앱
│   ├── seed_db.py              # 임시 데이터 추가
│   └── requirements.txt     # Python 패키지
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React 컴포넌트
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   ├── login.css
│   │   ├── login.jsx
│   │   ├── main.jsx
│   │   ├── Write.css
│   │   └── Write.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env                 # 환경 변수 (생성 필요)
└── README.md
