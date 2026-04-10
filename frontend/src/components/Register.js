import { useState } from "react";
import axios from "axios";
import "./Auth.css";

function Register({ setIsLoggedIn, switchToLogin }) {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirm_password: "",
    company: "",
    role: ""
  });

  const handleRegister = async () => {
    if (form.password !== form.confirm_password) {
      alert("Passwords do not match.");
      return;
    }

    try {
      const res = await axios.post("http://127.0.0.1:8000/register", form);

      if (res.data.success) {
        alert("Registration successful!");
        setIsLoggedIn(true);
      } else {
        alert(res.data.error || "Registration failed. Email may already be registered.");
      }
    } catch (error) {
      console.error("Register error:", error.response || error);
      alert("Server error. Please try again.");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">

        <h2>Create HR Account</h2>
        <p className="subtitle">Start hiring smarter with AI</p>

        <input placeholder="Full Name"
          value={form.name}
          onChange={(e) => setForm({...form, name: e.target.value})} />

        <input placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({...form, email: e.target.value})} />

        <input type="password" placeholder="Password"
          value={form.password}
          onChange={(e) => setForm({...form, password: e.target.value})} />

        <input type="password" placeholder="Confirm Password"
          value={form.confirm_password}
          onChange={(e) => setForm({...form, confirm_password: e.target.value})} />

        <input placeholder="Company"
          value={form.company}
          onChange={(e) => setForm({...form, company: e.target.value})} />

        <input placeholder="Role (HR/Recruiter)"
          value={form.role}
          onChange={(e) => setForm({...form, role: e.target.value})} />

        <button onClick={handleRegister}>Register</button>

        <p className="switch-text">
          Already have account? <span onClick={switchToLogin}>Login</span>
        </p>

      </div>
    </div>
  );
}

export default Register;