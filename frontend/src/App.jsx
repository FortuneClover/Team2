import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter, Routes, Route, Outlet, useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import LoginForm from './login.jsx';
import Write from './Write.jsx';

// 백엔드 서버 주소
const API_URL = "http://localhost:8000";
const POSTS_PER_PAGE = 5; // 한 번에 불러올 게시물 수

// --- 게시판 메인 페이지 컴포넌트 ---
function MainApp() {
    // --- 상태(State) 관리 ---
    const [posts, setPosts] = useState([]);
    const [user, setUser] = useState(null);
    const [page, setPage] = useState(0);
    const [hasMore, setHasMore] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const navigate = useNavigate();

    // --- 데이터 가져오기 함수 ---
    const fetchPosts = useCallback(async () => {
        if (!hasMore || loading) return;

        setLoading(true);
        setError(null);
        try {
            const skip = page * POSTS_PER_PAGE;
            const response = await axios.get(`${API_URL}/posts?skip=${skip}&limit=${POSTS_PER_PAGE}`);
            const newPosts = response.data.posts || [];
            
            setPosts(prevPosts => [...prevPosts, ...newPosts]);
            setHasMore(newPosts.length === POSTS_PER_PAGE);
            setPage(prevPage => prevPage + 1);

        } catch (err) { // 👈 버그 수정: catch 블록에 중괄호({})를 추가했습니다.
            console.error("게시물을 불러오는데 실패했습니다:", err);
            setError("게시물을 불러올 수 없습니다.");
        } finally {
            setLoading(false);
        }
    }, [page, hasMore, loading]);

    // --- useEffect Hooks ---
    useEffect(() => {
        const storedUser = sessionStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
        fetchPosts();
    }, []);

    // --- UI 렌더링 ---
    return (
        <>
            <header className="app-header">
                <div className="title-group">
                    <h1>게시판</h1>
                    {user && <p>{user.nickname}님, 환영합니다!</p>}
                </div>
                <button 
                    onClick={() => navigate('/Write')}
                    className="btn btn-primary"
                >
                    새 글 작성
                </button>
            </header>

            <main className="post-list">
                {posts.map(post => (
                    <div key={post.id} className="post-card">
                        <h2>{post.title}</h2>
                        <p>{post.content}</p>
                        {/* 👇 게시물 메타 정보 (장르 + 작성자) */}
                        <div className="post-meta">
                            {post.genre && <span className="genre-tag">{post.genre.name}</span>}
                            <span className="author-info">작성자: {post.author.nickname}</span>
                        </div>
                    </div>
                ))}
                
                {loading && <div className="text-center p-10">로딩 중...</div>}
                
                {hasMore && !loading && (
                    <div className="text-center p-4">
                        <button
                            onClick={fetchPosts}
                            className="btn btn-secondary"
                        >
                            더 보기
                        </button>
                    </div>
                )}

                {error && <div className="text-center p-10 text-red-500">{error}</div>}
                {!hasMore && posts.length > 0 && <div className="text-center p-10 text-gray-500">모든 게시물을 불러왔습니다.</div>}
                {!hasMore && posts.length === 0 && !loading && (
                    <div className="post-card text-center">
                        <p>아직 게시물이 없습니다.</p>
                    </div>
                )}
            </main>
        </>
    );
}

// --- 공통 레이아웃 컴포넌트 ---
function AppLayout() {
    return (
        <div className="app-container">
            <header className="app-layout-header">
                <a href="/App">Community Board</a>
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

