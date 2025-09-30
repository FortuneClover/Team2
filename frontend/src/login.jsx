import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";
import axios from 'axios';

// 백엔드 서버의 주소입니다. 환경에 맞게 수정할 수 있습니다.
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

      // --- ✅ 문제 해결 ---
      // 1. axios 응답 객체(res)에서 실제 데이터(res.data)를 추출합니다.
      const userData = res.data; 

      // 2. navigate 함수의 state에는 순수한 데이터(userData)만 전달합니다.
      //    이렇게 하면 MainApp 컴포넌트에서 로그인한 사용자 정보를 사용할 수 있습니다.
      //    경로도 '/App'이 아닌 컴포넌트 이름과 맞춘 '/main' 등으로 하는 것이 일반적이나,
      //    app.jsx 라우터 설정에 따라 '/App'으로 유지했습니다.
      navigate("/App", { state: { user: userData } });

    } catch (err) {
      console.error("Login failed:", err);
      setMessage("로그인 실패: 이메일 또는 비밀번호가 올바르지 않습니다.");
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
