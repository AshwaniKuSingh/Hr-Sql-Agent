import { useState } from "react"
import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

function Spinner() {
  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: "2rem" }}>
      <div style={{
        width: "40px",
        height: "40px",
        border: "4px solid #E0E7FF",
        borderTop: "4px solid #4F46E5",
        borderRadius: "50%",
        animation: "spin 1s linear infinite"
      }}/>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  )
}

function App() {
  const [question, setQuestion] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showSql, setShowSql] = useState(false)

  const handleQuery = async () => {
    if (!question.trim() || loading) return
    setLoading(true)
    setError(null)
    setResult(null)
    setShowSql(false)

    try {
      const response = await axios.post(`${API_URL}/query`, {
        question: question
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong")
    } finally {
      setLoading(false)
    }
  }

  const handleAskAgain = () => {
    setResult(null)
    setError(null)
    setQuestion("")
    setShowSql(false)
  }

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem" }}>
      <h1>HR Employee Assistant</h1>
      <p style={{ color: "#666" }}>Ask questions about the employee database in plain English</p>

      <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleQuery()}
          placeholder="e.g. How many employees are in each department?"
          disabled={loading}
          style={{
            flex: 1,
            padding: "0.75rem",
            fontSize: "1rem",
            borderRadius: "8px",
            border: "1px solid #ccc",
            opacity: loading ? 0.6 : 1
          }}
        />
        <button
          onClick={handleQuery}
          disabled={loading}
          style={{
            padding: "0.75rem 1.5rem",
            fontSize: "1rem",
            borderRadius: "8px",
            background: loading ? "#A5B4FC" : "#4F46E5",
            color: "white",
            border: "none",
            cursor: loading ? "not-allowed" : "pointer",
            transition: "background 0.2s"
          }}
        >
          Ask
        </button>
      </div>

      {loading && (
        <>
          <Spinner />
          <p style={{ textAlign: "center", color: "#6366F1", marginTop: "0.5rem" }}>
            Thinking... this may take a moment
          </p>
        </>
      )}

      {error && !loading && (
        <div style={{ marginTop: "1rem", padding: "1rem", background: "#FEE2E2", borderRadius: "8px", color: "#991B1B" }}>
          {error}
          <div style={{ marginTop: "0.75rem" }}>
            <button
              onClick={handleAskAgain}
              style={{ padding: "0.5rem 1rem", borderRadius: "6px", border: "1px solid #991B1B", background: "none", color: "#991B1B", cursor: "pointer" }}
            >
              Try again
            </button>
          </div>
        </div>
      )}

      {result && !loading && (
        <div style={{ marginTop: "1.5rem" }}>
          <div style={{ padding: "1rem", background: "#F0FDF4", borderRadius: "8px", color: "#166534", lineHeight: "1.6" }}>
            {result.rows}
          </div>

          {result.sql && (
            <div style={{ marginTop: "1rem" }}>
              <button
                onClick={() => setShowSql(!showSql)}
                style={{ background: "none", border: "1px solid #ccc", padding: "0.5rem 1rem", borderRadius: "6px", cursor: "pointer" }}
              >
                {showSql ? "Hide SQL" : "Show SQL"}
              </button>
              {showSql && (
                <pre style={{ marginTop: "0.5rem", padding: "1rem", background: "#1E1E1E", color: "#D4D4D4", borderRadius: "8px", overflow: "auto" }}>
                  {result.sql}
                </pre>
              )}
            </div>
          )}

          <div style={{ marginTop: "1rem" }}>
            <button
              onClick={handleAskAgain}
              style={{
                padding: "0.75rem 1.5rem",
                fontSize: "1rem",
                borderRadius: "8px",
                background: "#4F46E5",
                color: "white",
                border: "none",
                cursor: "pointer"
              }}
            >
              Ask another question
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default App