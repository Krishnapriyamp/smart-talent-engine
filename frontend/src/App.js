import { useState } from "react";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import Login from "./components/Login";
import Register from "./components/Register";
import "./App.css";

function App() {
  const [currentPage, setCurrentPage] = useState("upload");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  if (!isLoggedIn) {
    return showRegister ? (
      <Register setIsLoggedIn={setIsLoggedIn} switchToLogin={() => setShowRegister(false)} />
    ) : (
      <Login setIsLoggedIn={setIsLoggedIn} switchToRegister={() => setShowRegister(true)} />
    );
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1 className="title">Smart Talent Selection System</h1>
        <div className="nav-buttons">
          <button onClick={() => setCurrentPage("upload")}>Upload Resumes</button>
          <button onClick={() => setCurrentPage("dashboard")}>Dashboard</button>
          <button className="logout-button" onClick={() => setIsLoggedIn(false)}>
            Logout
          </button>
        </div>
      </header>
      <main>
        {currentPage === "upload" ? <Upload /> : <Dashboard />}
      </main>
    </div>
  );
}

export default App;