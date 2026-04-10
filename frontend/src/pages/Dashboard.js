import { useState } from "react";
import axios from "axios";
import "./Dashboard.css";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell
} from "recharts";

function Dashboard() {
  const [jd, setJd] = useState("");
  const [skills, setSkills] = useState("");
  const [exp, setExp] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const rank = async () => {
    try {
      setLoading(true);
      const res = await axios.post("http://127.0.0.1:8000/rank", {
        text: jd,
        skills: skills.split(",").map(s => s.trim()).filter(s => s !== ""),
        experience: parseInt(exp) || 0
      });

      console.log("API RESPONSE:", res.data);

      // ✅ FIX: ensure it's an array
      if (Array.isArray(res.data)) {
        setResults(res.data);
      } else {
        alert("No resumes uploaded OR backend error ❌");
        setResults([]);
      }

    } catch (error) {
      console.error("RANK ERROR:", error);
      alert("Ranking failed ❌ Check backend");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">

      {/* Job Description */}
      <div className="card">
        <h2>Job Description</h2>

        <textarea
          placeholder="Enter Job Description..."
          onChange={(e) => setJd(e.target.value)}
        />

        <input
          placeholder="Skills (python, sql, ml)"
          onChange={(e) => setSkills(e.target.value)}
        />

        <input
          type="number"
          placeholder="Minimum Experience (years)"
          onChange={(e) => setExp(e.target.value)}
        />

        <button onClick={rank} disabled={loading}>
          {loading ? "Ranking..." : "Rank Candidates"}
        </button>
      </div>

      {/* Chart */}
      {Array.isArray(results) && results.length > 0 && (
        <div className="card">
          <h3>Candidate Score Comparison</h3>

          <BarChart width={600} height={300} data={results}>
            <CartesianGrid stroke="none" />

            <XAxis
              dataKey="name"
              axisLine={false}
              tickLine={false}
            />

            <YAxis axisLine={false} tickLine={false} />

            <Tooltip />

            <Bar dataKey="score" barSize={40}>
              {results.map((entry, index) => (
                <Cell
                  key={index}
                  fill={
                    entry.score >= 70
                      ? "#4CAF50"
                      : entry.score >= 40
                      ? "#FFC107"
                      : "#F44336"
                  }
                />
              ))}
            </Bar>
          </BarChart>
        </div>
      )}

      {/* Results */}
      <div className="grid">
        {Array.isArray(results) && results.map((c, i) => (
          <div className={`result-card ${i === 0 ? "top-candidate" : ""}`} key={i}>

            <div className="result-header">
              <div>
                <h3>
                  #{i + 1} {c.name}
                </h3>
                <p className="subtext">{c.verdict}</p>
              </div>
              {i === 0 && <span className="badge gold">Top Candidate</span>}
            </div>

            <div className="score-pill" style={{ background: c.color }}>
              <strong>{c.score}%</strong>
              <div className="confidence-container">
                <span>Confidence {c.confidence}%</span>
                <span className="info-icon" title={c.confidence_explanation}>ℹ️</span>
              </div>
            </div>

            {c.penalty > 0 && (
              <p className="warning">Penalty: -{c.penalty}</p>
            )}

            <div className="info-grid">
              <div>
                <h4>Extracted Skills</h4>
                <p>{c.extracted_skills?.join(", ") || c.skills?.join(", ") || "No skills found"}</p>
              </div>
              <div>
                <h4>Experience</h4>
                <p>{(c.exp_details || c.experience)?.years || 0} years</p>
                <p>{(c.exp_details || c.experience)?.projects || 0} projects</p>
                <p>{(c.exp_details || c.experience)?.certifications || 0} certifications</p>
                <p>{(c.exp_details || c.experience)?.work_exp || 0} work/internship</p>
              </div>
            </div>

            <div className="skill-row">
              <div>
                <h4>Matched Skills</h4>
                <p className="matched">{c.matched_skills?.join(", ") || "None"}</p>
              </div>
              <div>
                <h4>Missing Skills</h4>
                <p className="missing">{c.missing_skills?.join(", ") || "None"}</p>
              </div>
            </div>

            <div className="breakdown">
              <h4>Score Breakdown</h4>
              <p>Semantic: <strong>{c.semantic}%</strong></p>
              <p>Skill: <strong>{c.skill}%</strong></p>
              <p>Experience: <strong>{c.experience_score}%</strong></p>
            </div>

            <div className="explanation-box">
              <h4>Explanation</h4>
              <p>{c.explanation}</p>
              {c.strengths?.length > 0 && (
                <div>
                  <h5>Strengths</h5>
                  <ul>
                    {c.strengths.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
              {c.weaknesses?.length > 0 && (
                <div>
                  <h5>Weaknesses</h5>
                  <ul>
                    {c.weaknesses.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

          </div>
        ))}
      </div>

    </div>
  );
}

export default Dashboard;