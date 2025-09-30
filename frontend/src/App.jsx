import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Outlet, useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import LoginForm from './login.jsx';
import Write from './Write.jsx';

// 백엔드 서버 주소
const API_URL = "http://localhost:8000";

// --- 게시판 메인 페이지 컴포넌트 ---
function MainApp() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const location = useLocation();
  const navigate = useNavigate();
  
  const user = location.state?.user;

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get(`${API_URL}/posts`);
        // 백엔드 응답 형식에 맞게 데이터 설정
        setPosts(response.data.posts || []); 
      } catch (err) {
        console.error("게시물을 불러오는데 실패했습니다:", err);
        setError("게시물을 불러올 수 없습니다.");
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []);

  if (loading) return <div className="text-center p-10">로딩 중...</div>;
  if (error) return <div className="text-center p-10 text-red-500">{error}</div>;

  return (
    <>
      {/* 헤더 부분: app-header 클래스 적용 */}
      <header className="app-header">
        <div className="title-group">
          <h1>게시판</h1>
          {user && <p>{user.nickname}님, 환영합니다!</p>}
        </div>
        {/* 버튼: btn 및 btn-primary 클래스 적용 */}
        <button 
          onClick={() => navigate('/Write')}
          className="btn btn-primary"
        >
          새 글 작성
        </button>
      </header>

      {/* 게시물 목록: post-list 클래스 적용 */}
      <main className="post-list">
        {posts.length > 0 ? (
          posts.map(post => (
            // 각 게시물: post-card 클래스 적용
            <div key={post.id} className="post-card">
              <h2>{post.title}</h2>
              <p>{post.content}</p>
              <div className="author-info">
                <span>작성자: {post.author ? post.author.nickname : '알 수 없음'}</span>
              </div>
            </div>
          ))
        ) : (
          <div className="post-card text-center">
            <p>아직 게시물이 없습니다. 첫 번째 게시물을 작성해보세요!</p>
          </div>
        )}
      </main>
    </>
  );
}

// --- 공통 레이아웃 컴포넌트 ---
function AppLayout() {
  return (
    <div>
      <header style={{ padding: '1rem', borderBottom: '1px solid #444', textAlign: 'center' }}>
        <a href="/App" style={{ textDecoration: 'none', color: '#A0AEC0' }}>Community Board</a>
      </header>
      <main>
        <Outlet /> 
      </main>
    </div>
  );
}

// --- 라우터 설정 ---
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginForm />} />
      <Route element={<AppLayout />}>
        <Route path="/App" element={<MainApp />} />
        <Route path="/Write" element={<Write />} />
      </Route>
      <Route path="*" element={<div>404 Not Found</div>} />
    </Routes>
  );
}

