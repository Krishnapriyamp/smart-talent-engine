import { useState } from "react";
import axios from "axios";
import "./Login.css";

function Login({ setIsLoggedIn, switchToRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/login", {
        email,
        password,
      });

      if (res.data.success) {
        setIsLoggedIn(true);
      } else {
        alert(res.data.error || "Invalid credentials");
      }
    } catch (error) {
      console.error("Login error:", error.response || error);
      alert("Server error. Please try again.");
    }
  };

  return (
    <div className="login-container">

      {/* LEFT SIDE */}
      <div className="login-left">
        <h1>Smart Talent Portal</h1>
        <p className="tagline">
          AI-driven platform for efficient and intelligent hiring.
        </p>

        <div className="features">
          <p><strong>Efficient Candidate Discovery</strong></p>
          <p><strong>AI-Driven Skill Evaluation</strong></p>
          <p><strong>Intelligent Ranking System</strong></p>
          <p><strong>Faster Recruitment Process</strong></p>
        </div>

        <div className="quote">
          <p>"Empowering smarter hiring through technology."</p>
        </div>
      </div>

      {/* RIGHT SIDE */}
      <div className="login-right">
        <div className="login-card">
          <h2>Welcome Back</h2>
          <p className="subtitle">Login to your account</p>

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button onClick={handleLogin}>Login</button>

          <p className="switch-text">
            New here? <span onClick={switchToRegister}>Create account</span>
          </p>
        </div>
      </div>

    </div>
  );
}

export default Login;