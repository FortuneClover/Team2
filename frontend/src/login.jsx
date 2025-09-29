import React, { useState } from "react";
import "./login.css";

const API_URL = "http://localhost:8000";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await axios.patch(`${API_URL}/login`, {
        user_id: email.trim(),
        pd: password.trim()
    })

    console.log(res);
    // setMessage(data.message);
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

        {message && <p>{message}</p>}
      </div>
    </div>
  );
}