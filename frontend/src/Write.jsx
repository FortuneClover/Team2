import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './write.css'; // 글쓰기 폼 전용 CSS 임포트

// 백엔드 서버 주소
const API_URL = "http://localhost:8000";

export default function Write() {
    const navigate = useNavigate();
    
    // --- 상태(State) 관리 ---
    // 사용자 정보
    const [user, setUser] = useState(null);

    // 폼 입력 값
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [selectedGenreId, setSelectedGenreId] = useState(''); // 선택된 장르 ID

    // UI 상태
    const [genres, setGenres] = useState([]); // 장르 목록
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    // --- useEffect Hooks ---
    // 1. 컴포넌트 마운트 시 사용자 정보와 장르 목록을 불러옵니다.
    useEffect(() => {
        // 세션 스토리지에서 사용자 정보 가져오기
        const storedUser = sessionStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        } else {
            setError('로그인 정보가 없습니다. 다시 로그인해주세요.');
        }

        // 백엔드에서 장르 목록 가져오기
        const fetchGenres = async () => {
            try {
                const response = await axios.get(`${API_URL}/genres`);
                setGenres(response.data.genres || []);
            } catch (err) {
                console.error("장르 목록을 불러오는데 실패했습니다:", err);
                setError("장르 목록을 불러올 수 없습니다.");
            }
        };

        fetchGenres();
    }, []); // 빈 배열을 전달하여 한 번만 실행

    // --- 이벤트 핸들러 ---
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // 유효성 검사
        if (!user) {
            setError('로그인 정보가 필요합니다.');
            return;
        }
        if (!title.trim() || !content.trim()) {
            setError('제목과 내용을 모두 입력해주세요.');
            return;
        }
        if (!selectedGenreId) {
            setError('장르를 선택해주세요.');
            return;
        }
        
        setIsSubmitting(true);
        setError('');
        setSuccess('');

        try {
            const newPostData = {
                title: title.trim(),
                content: content.trim(),
                user_id: user.id,
                genre_id: parseInt(selectedGenreId, 10), // 선택된 장르 ID를 정수로 변환
            };
            
            await axios.post(`${API_URL}/posts`, newPostData);
            
            setSuccess('게시물이 성공적으로 등록되었습니다! 잠시 후 게시판으로 이동합니다.');

            setTimeout(() => navigate('/App'), 1500);

        } catch (err) {
            setError('게시물 등록에 실패했습니다. 다시 시도해주세요.');
            console.error(err);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="write-container">
            <h1>새 글 작성하기</h1>
            
            <form onSubmit={handleSubmit}>
                {/* 제목 입력 */}
                <div className="form-group">
                    <label htmlFor="title">제목</label>
                    <input
                        id="title"
                        type="text"
                        placeholder="게시물 제목을 입력하세요"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        className="form-input"
                    />
                </div>

                {/* 장르 선택 드롭다운 (신규 추가) */}
                <div className="form-group">
                    <label htmlFor="genre">장르</label>
                    <select
                        id="genre"
                        value={selectedGenreId}
                        onChange={(e) => setSelectedGenreId(e.target.value)}
                        className="form-input" // 동일한 스타일 재사용
                    >
                        <option value="" disabled>-- 장르를 선택하세요 --</option>
                        {genres.map((genre) => (
                            <option key={genre.id} value={genre.id}>
                                {genre.name}
                            </option>
                        ))}
                    </select>
                </div>

                {/* 내용 입력 */}
                <div className="form-group">
                    <label htmlFor="content">내용</label>
                    <textarea
                        id="content"
                        placeholder="내용을 입력하세요"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        rows={10}
                        className="form-textarea"
                    />
                </div>
                
                {/* 성공 및 에러 메시지 */}
                {success && <div className="message-box message-success">{success}</div>}
                {error && <div className="message-box message-error">{error}</div>}

                {/* 버튼 영역 */}
                <div className="form-actions">
                    <button type="button" onClick={() => navigate('/App')} className="btn btn-secondary">
                        취소
                    </button>
                    <button type="submit" disabled={isSubmitting} className="btn btn-primary">
                        {isSubmitting ? '등록 중...' : '게시물 등록'}
                    </button>
                </div>
            </form>
        </div>
    );
};

