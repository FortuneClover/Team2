import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './write.css'; // 👈 CSS 파일을 임포트합니다.

// 백엔드 서버 주소
const API_URL = "http://localhost:8000";

export default function Write() {
  const navigate = useNavigate();

  // 사용자 정보를 컴포넌트의 state로 관리합니다.
  const [user, setUser] = useState(null);

  // 폼 상태 관리
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // ✅ 컴포넌트가 처음 로드될 때 sessionStorage에서 사용자 정보를 가져옵니다.
  useEffect(() => {
    const storedUser = sessionStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      setError('로그인 정보가 없습니다. 다시 로그인해주세요.');
    }
  }, []); // 빈 의존성 배열로 최초 1회만 실행

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) {
      setError('제목과 내용을 모두 입력해주세요.');
      return;
    }
    // ✅ state에 저장된 user 정보를 확인합니다.
    if (!user || !user.id) {
      setError('사용자 정보가 없어 게시물을 작성할 수 없습니다. 다시 로그인해주세요.');
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
        genre_id: 1 // TODO: 장르 선택 기능 추가
      };
      
      await axios.post(`${API_URL}/posts`, newPostData);
      
      setSuccess('게시물이 성공적으로 등록되었습니다! 잠시 후 게시판으로 이동합니다.');

      setTimeout(() => {
        navigate('/App');
      }, 1500);

    } catch (err) {
      setError('게시물 등록에 실패했습니다. 다시 시도해주세요.');
      console.error(err);
      setIsSubmitting(false);
    }
  };

  return (
    <div className="write-container">
      <h1>새 글 작성하기</h1>
      
      <form onSubmit={handleSubmit}>
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

        <div className="form-group">
          <label htmlFor="content">내용</label>
          <textarea
            id="content"
            placeholder="내용을 입력하세요"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={8}
            className="form-textarea"
          />
        </div>
        
        {success && <div className="message-box message-success">{success}</div>}
        {error && <div className="message-box message-error">{error}</div>}

        <div className="form-actions">
          <button
            type="button"
            onClick={() => navigate('/App')}
            className="btn btn-secondary"
          >
            취소
          </button>
          <button
            type="submit"
            disabled={isSubmitting || !user} // 사용자 정보가 없으면 버튼 비활성화
            className="btn btn-primary"
          >
            {isSubmitting ? '등록 중...' : '게시물 등록'}
          </button>
        </div>
      </form>
    </div>
  );
};

