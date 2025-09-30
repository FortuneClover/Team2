import React, { useState, useEffect } from 'react';
import { Routes, Route, Outlet, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

// 컴포넌트 임포트
import LoginForm from './login.jsx';
import Write from './Write.jsx';

// CSS 임포트
import './App.css';

// 백엔드 서버 주소
const API_URL = "http://localhost:8000";

// --- 공통 레이아웃 컴포넌트 ---
function AppLayout() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  // 레이아웃이 로드될 때 sessionStorage에서 사용자 정보를 확인합니다.
  useEffect(() => {
    const storedUser = sessionStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  // 로그아웃 핸들러
  const handleLogout = () => {
    sessionStorage.removeItem('user'); // sessionStorage에서 사용자 정보 제거
    setUser(null); // 상태 업데이트
    navigate('/'); // 로그인 페이지로 이동
  };

  return (
    <div className="app-container">
      <nav className="main-nav">
        <Link to="/App" className="nav-logo">Community Board</Link>
        <div>
          {user ? (
            <button onClick={handleLogout} className="btn">로그아웃</button>
          ) : (
            <button onClick={() => navigate('/')} className="btn">로그인</button>
          )}
        </div>
      </nav>
      <main>
        {/* 자식 라우트 컴포넌트가 여기에 렌더링됩니다. */}
        <Outlet />
      </main>
    </div>
  );
}

// --- 게시판 메인 페이지 컴포넌트 ---
function MainApp() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null); // 사용자 정보 상태
  const navigate = useNavigate();

  useEffect(() => {
    // ✅ 컴포넌트가 마운트될 때 sessionStorage에서 사용자 정보를 가져옵니다.
    const storedUser = sessionStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }

    const fetchPosts = async () => {
      try {
        const response = await axios.get(`${API_URL}/posts`);
        setPosts(response.data.posts || []);
      } catch (err) {
        console.error("게시물을 불러오는데 실패했습니다:", err);
        setError("게시물을 불러올 수 없습니다.");
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []); // 최초 1회 실행

  if (loading) return <div className="loading-message">로딩 중...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <>
      <header className="app-header">
        <div className="title-group">
          <h1>게시판</h1>
          {/* ✅ state에 저장된 user 정보로 환영 메시지를 표시합니다. */}
          {user && <p>{user.nickname}님, 환영합니다!</p>}
        </div>
        <button 
          className="btn btn-primary" 
          // ✅ 글쓰기 페이지로 이동할 때 더 이상 state를 넘길 필요가 없습니다.
          onClick={() => navigate('/Write')}
        >
          새 글 작성
        </button>
      </header>

      <div className="post-list">
        {posts.length > 0 ? (
          posts.map(post => (
            <div key={post.id} className="post-card">
              <h2>{post.title}</h2>
              <p>{post.content}</p>
              <div className="author-info">
                <span>작성자: {post.author ? post.author.nickname : '알 수 없음'}</span>
              </div>
            </div>
          ))
        ) : (
          <div className="no-posts-message">아직 게시물이 없습니다.</div>
        )}
      </div>
    </>
  );
}

// --- 라우터 설정 ---
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginForm />} />
      {/* AppLayout이 /App과 /Write 경로를 감쌉니다. */}
      <Route element={<AppLayout />}>
        <Route path="/App" element={<MainApp />} />
        <Route path="/Write" element={<Write />} />
      </Route>
      <Route path="*" element={<div>404 Not Found</div>} />
    </Routes>
  );
}

