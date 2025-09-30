import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";
import axios from 'axios';

// 백엔드 서버의 주소입니다.
const API_URL = "http://localhost:8000";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // 서버로 로그인 요청을 보냅니다.
      const res = await axios.post(`${API_URL}/login`, {
        email: email.trim(),
        password: password.trim(),
      });
      
      const userData = res.data;

      // --- ✅ sessionStorage 로직 적용 ---
      // 1. 받아온 사용자 정보를 JSON 문자열 형태로 sessionStorage에 저장합니다.
      //    이제 브라우저를 새로고침해도 로그인 정보가 유지됩니다.
      sessionStorage.setItem('user', JSON.stringify(userData));

      // 2. 게시판 페이지로 이동시킵니다.
      navigate("/App");

    } catch (err) {
      console.error("Login failed:", err);
      // 백엔드에서 보낸 에러 메시지가 있다면 표시, 없다면 기본 메시지
      const detail = err.response?.data?.detail;
      setMessage(detail || "로그인 실패: 이메일 또는 비밀번호가 올바르지 않습니다.");
    }
  };

  return (
    <div className="container">
      <h1 className="app-title">Login</h1>
      <div className="login-box">
        <form onSubmit={handleSubmit}>
          <h1>로그인</h1>

          <div className="input-group">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="login-options">
            <div className="remember-me">
              <input
                type="checkbox"
                checked={remember}
                onChange={(e) => setRemember(e.target.checked)}
              />
              <label>Remember me</label>
            </div>
            <a href="#" className="forgot-password">
              Forgot password?
            </a>
          </div>

          <button type="submit" className="login-button">
            Login
          </button>
        </form>

        <div className="signup-link">
          <p>
            Don’t have an account? <a href="#">Sign up</a>
          </p>
        </div>

        {message && <p className="error-message">{message}</p>}
      </div>
    </div>
  );
}

