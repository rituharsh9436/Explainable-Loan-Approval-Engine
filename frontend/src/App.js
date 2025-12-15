// Harsh Bhardwaj
import { useState, useEffect } from "react";

function App() {
  useEffect(() => {
    document.title = "Loan Approval Engine";
  }, []);

  const [form, setForm] = useState({
    Gender: "Male",
    Married: "Yes",
    Dependents: "0",
    Education: "Graduate",
    Employment_Status: "Salaried",
    Applicant_Income: 5000,
    Coapplicant_Income: 0,
    Loan_Amount: 200,
    Loan_Term: 360,
    Credit_History: 1,
    Property_Area: "Urban",
    Age: 30
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const update = (k, v) => setForm({ ...form, [k]: v });

  const predict = async () => {
    setLoading(true);
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <header style={styles.header}>
          <h1>Loan Approval Engine</h1>
          <p>
            A transparent machine learning system for credit risk assessment
            with interpretable decisions and consistent feature analysis.
            using XGBoost and SHAP.
          </p>
        </header>

        <div style={styles.grid}>
          {/* Financial Information */}
          <Card title="Financial Information">
            <Slider
              label="Applicant Income"
              unit="₹"
              value={form.Applicant_Income}
              min={0}
              max={140000}
              step={500}
              onChange={(v) => update("Applicant_Income", v)}
            />

            <Slider
              label="Coapplicant Income"
              unit="₹"
              value={form.Coapplicant_Income}
              min={0}
              max={50000}
              step={500}
              onChange={(v) => update("Coapplicant_Income", v)}
            />

            <Slider
              label="Loan Amount"
              unit="₹"
              value={form.Loan_Amount}
              min={0}
              max={380000}
              step={0.5}
              onChange={(v) => update("Loan_Amount", v)}
            />
          </Card>

          {/* Credit Profile */}
          <Card title="Credit Profile">
            <Select
              label="Credit History"
              value={form.Credit_History}
              options={{ 1: "Good", 0: "Poor" }}
              onChange={(v) => update("Credit_History", Number(v))}
            />

            <Slider
              label="Loan Term"
              unit="months"
              value={form.Loan_Term}
              min={60}
              max={480}
              step={12}
              onChange={(v) => update("Loan_Term", v)}
            />
          </Card>

          {/* Applicant Details */}
          <Card title="Applicant Details">
            <Select
              label="Gender"
              value={form.Gender}
              options={{ Male: "Male", Female: "Female" }}
              onChange={(v) => update("Gender", v)}
            />

            <Select
              label="Marital Status"
              value={form.Married}
              options={{ Yes: "Married", No: "Single" }}
              onChange={(v) => update("Married", v)}
            />

            <Select
              label="Employment Status"
              value={form.Employment_Status}
              options={{
                "Salaried": "Salaried",
                "Self-Employed": "Self-Employed"
              }}
              onChange={(v) => update("Employment_Status", v)}
            />

            <Slider
              label="Age"
              value={form.Age}
              min={18}
              max={65}
              step={1}
              onChange={(v) => update("Age", v)}
            />
          </Card>
        </div>

        <button style={styles.button} onClick={predict}>
          {loading ? "Evaluating application..." : "Evaluate Loan Application"}
        </button>

        {result && (
          <div style={styles.result}>
            <h2
              style={{
                color:
                  result.decision === "Approved"
                    ? "#00d4a3"
                    : "#ff6b6b"
              }}
            >
              {result.decision}
            </h2>
            <p>
              Approval Probability:{" "}
              <strong>{result.approval_probability}</strong>
            </p>
            <p style={styles.note}>
              Decision supported by model explainability and feature-level
              contribution analysis.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/* ---------- COMPONENTS ---------- */

const Card = ({ title, children }) => (
  <div style={styles.card}>
    <h3>{title}</h3>
    {children}
  </div>
);

const Slider = ({ label, value, min, max, step, unit, onChange }) => (
  <div style={styles.field}>
    <label>{label}</label>
    <input
      type="range"
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
    />
    <span>{unit ? `${value} ${unit}` : value}</span>
  </div>
);

const Select = ({ label, value, options, onChange }) => (
  <div style={styles.field}>
    <label>{label}</label>
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={styles.select}
    >
      {Object.entries(options).map(([k, v]) => (
        <option
          key={k}
          value={k}
          style={{ background: "#1f3b4d", color: "#ffffff" }}
        >
          {v}
        </option>
      ))}
    </select>
  </div>
);

/* ---------- STYLES ---------- */

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg,#0b1f2a,#162d3a,#1f3b4d)",
    color: "#ffffff",
    display: "flex",
    justifyContent: "center",
    padding: "32px"
  },
  container: {
    width: "1100px"
  },
  header: {
    marginBottom: "28px"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: "22px"
  },
  card: {
    background: "rgba(255,255,255,0.08)",
    backdropFilter: "blur(14px)",
    padding: "22px",
    borderRadius: "16px",
    boxShadow: "0 12px 32px rgba(0,0,0,0.45)"
  },
  field: {
    display: "flex",
    flexDirection: "column",
    marginBottom: "14px"
  },
  select: {
    padding: "10px 12px",
    borderRadius: "12px",
    border: "1px solid rgba(255,255,255,0.2)",
    background: "rgba(255,255,255,0.08)",
    color: "#ffffff",
    fontSize: "14px",
    outline: "none",
    cursor: "pointer",
    appearance: "none",
    WebkitAppearance: "none",
    MozAppearance: "none"
  },
  button: {
    marginTop: "28px",
    width: "100%",
    padding: "15px",
    borderRadius: "14px",
    border: "none",
    fontSize: "16px",
    fontWeight: "700",
    background: "linear-gradient(135deg,#00b4db,#0083b0)",
    color: "#ffffff",
    cursor: "pointer"
  },
  result: {
    marginTop: "28px",
    padding: "24px",
    background: "rgba(0,0,0,0.4)",
    borderRadius: "16px",
    textAlign: "center"
  },
  note: {
    fontSize: "13px",
    opacity: 0.75,
    marginTop: "8px"
  }
};

export default App;