// Harsh Bhardwaj
import { useEffect, useState } from "react";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

const initialForm = {
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
};

async function postJson(path, payload) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || data.error || `Request failed with ${response.status}`);
  }

  return data;
}

function App() {
  useEffect(() => {
    document.title = "Loan Approval Engine";
  }, []);

  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [shap, setShap] = useState(null);
  const [lime, setLime] = useState(null);
  const [error, setError] = useState("");
  const [shapError, setShapError] = useState("");
  const [limeError, setLimeError] = useState("");
  const [loading, setLoading] = useState(false);
  const [explanationTab, setExplanationTab] = useState("shap");

  const update = (key, value) => setForm((current) => ({ ...current, [key]: value }));

  const predict = async () => {
    setLoading(true);
    setResult(null);
    setShap(null);
    setLime(null);
    setError("");
    setShapError("");
    setLimeError("");

    try {
      const prediction = await postJson("/predict", form);
      setResult(prediction);

      const [shapResult, limeResult] = await Promise.allSettled([
        postJson("/explain/shap", form),
        postJson("/explain/lime", form)
      ]);

      if (shapResult.status === "fulfilled") {
        setShap(shapResult.value);
      } else {
        setShapError(shapResult.reason.message);
      }

      if (limeResult.status === "fulfilled") {
        setLime(limeResult.value);
      } else {
        setLimeError(limeResult.reason.message);
      }
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <header style={styles.header}>
          <h1>Loan Approval Engine</h1>
          <p>
            A transparent machine learning system for credit risk assessment
            with interpretable decisions and consistent feature analysis.
            Using XGBoost with SHAP and LIME explanations.
          </p>
        </header>

        <div style={styles.grid}>
          <Card title="Financial Information">
            <Slider
              label="Applicant Income"
              unit="INR"
              value={form.Applicant_Income}
              min={0}
              max={140000}
              step={500}
              onChange={(value) => update("Applicant_Income", value)}
            />

            <Slider
              label="Coapplicant Income"
              unit="INR"
              value={form.Coapplicant_Income}
              min={0}
              max={50000}
              step={500}
              onChange={(value) => update("Coapplicant_Income", value)}
            />

            <Slider
              label="Loan Amount"
              unit="INR"
              value={form.Loan_Amount}
              min={1}
              max={380000}
              step={0.5}
              onChange={(value) => update("Loan_Amount", value)}
            />
          </Card>

          <Card title="Credit Profile">
            <Select
              label="Credit History"
              value={form.Credit_History}
              options={{ 1: "Good", 0: "Poor" }}
              onChange={(value) => update("Credit_History", Number(value))}
            />

            <Slider
              label="Loan Term"
              unit="months"
              value={form.Loan_Term}
              min={60}
              max={480}
              step={12}
              onChange={(value) => update("Loan_Term", value)}
            />

            <Select
              label="Property Area"
              value={form.Property_Area}
              options={{ Rural: "Rural", Semiurban: "Semiurban", Urban: "Urban" }}
              onChange={(value) => update("Property_Area", value)}
            />
          </Card>

          <Card title="Applicant Details">
            <Select
              label="Gender"
              value={form.Gender}
              options={{ Male: "Male", Female: "Female" }}
              onChange={(value) => update("Gender", value)}
            />

            <Select
              label="Marital Status"
              value={form.Married}
              options={{ Yes: "Married", No: "Single" }}
              onChange={(value) => update("Married", value)}
            />

            <Select
              label="Dependents"
              value={form.Dependents}
              options={{ 0: "0", 1: "1", 2: "2", "3+": "3+" }}
              onChange={(value) => update("Dependents", value)}
            />

            <Select
              label="Education"
              value={form.Education}
              options={{ Graduate: "Graduate", "Not Graduate": "Not Graduate" }}
              onChange={(value) => update("Education", value)}
            />

            <Select
              label="Employment Status"
              value={form.Employment_Status}
              options={{
                Salaried: "Salaried",
                "Self-Employed": "Self-Employed",
                Unemployed: "Unemployed"
              }}
              onChange={(value) => update("Employment_Status", value)}
            />

            <Slider
              label="Age"
              value={form.Age}
              min={18}
              max={100}
              step={1}
              onChange={(value) => update("Age", value)}
            />
          </Card>
        </div>

        <button style={styles.button} onClick={predict} disabled={loading}>
          {loading ? "Evaluating application..." : "Evaluate Loan Application"}
        </button>

        {error && <div style={styles.error}>{error}</div>}

        {result && (
          <div style={styles.result}>
            <h2 style={{ color: result.decision === "Approved" ? "#00d4a3" : "#ff6b6b" }}>
              {result.decision}
            </h2>
            <p>
              Approval Probability: <strong>{result.approval_probability}</strong>
            </p>

            <div style={styles.explanationSection}>
              <div style={styles.tabs}>
                <button
                  style={{
                    ...styles.tab,
                    ...(explanationTab === "shap" ? styles.tabActive : styles.tabInactive)
                  }}
                  onClick={() => setExplanationTab("shap")}
                >
                  SHAP Explanation
                </button>
                <button
                  style={{
                    ...styles.tab,
                    ...(explanationTab === "lime" ? styles.tabActive : styles.tabInactive)
                  }}
                  onClick={() => setExplanationTab("lime")}
                >
                  LIME Explanation
                </button>
              </div>

              {explanationTab === "shap" && (
                <ExplanationMessage error={shapError}>
                  {shap?.shap_values && (
                    <div style={styles.explanationContent}>
                      <h3>SHAP Feature Contributions</h3>
                      <p style={styles.baseValue}>
                        Base Value: <strong>{Number(shap.base_value).toFixed(4)}</strong>
                      </p>
                      <FeatureBars features={shap.shap_values} />
                    </div>
                  )}
                </ExplanationMessage>
              )}

              {explanationTab === "lime" && (
                <ExplanationMessage error={limeError}>
                  {lime?.lime_features && (
                    <div style={styles.explanationContent}>
                      <h3>LIME Local Explanations</h3>
                      <div style={styles.features}>
                        {Object.entries(lime.lime_features).map(([feature, value]) => (
                          <div key={feature} style={styles.featureRow}>
                            <span style={styles.featureName}>{feature}</span>
                            <span style={styles.featureValue}>{Number(value).toFixed(4)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </ExplanationMessage>
              )}
            </div>

            <p style={styles.note}>
              Decision supported by model explainability and feature-level contribution analysis.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

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
      onChange={(event) => onChange(Number(event.target.value))}
    />
    <span>{unit ? `${value} ${unit}` : value}</span>
  </div>
);

const Select = ({ label, value, options, onChange }) => (
  <div style={styles.field}>
    <label>{label}</label>
    <select value={value} onChange={(event) => onChange(event.target.value)} style={styles.select}>
      {Object.entries(options).map(([key, labelText]) => (
        <option key={key} value={key} style={{ background: "#1f3b4d", color: "#ffffff" }}>
          {labelText}
        </option>
      ))}
    </select>
  </div>
);

const ExplanationMessage = ({ error, children }) => {
  if (error) {
    return <p style={styles.warning}>{error}</p>;
  }

  return children || <p style={styles.warning}>Explanation is not available.</p>;
};

const FeatureBars = ({ features }) => (
  <div style={styles.features}>
    {Object.entries(features)
      .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
      .slice(0, 10)
      .map(([feature, value]) => (
        <div key={feature} style={styles.featureRow}>
          <span style={styles.featureName}>{feature}</span>
          <div style={styles.bar}>
            <div
              style={{
                ...styles.barFill,
                width: `${Math.min(Math.abs(value) * 100, 100)}%`,
                background: value > 0 ? "#00d4a3" : "#ff6b6b"
              }}
            />
          </div>
          <span style={styles.featureValue}>{Number(value).toFixed(4)}</span>
        </div>
      ))}
  </div>
);

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
    width: "min(1100px, 100%)"
  },
  header: {
    marginBottom: "28px"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
    gap: "22px"
  },
  card: {
    background: "rgba(255,255,255,0.08)",
    backdropFilter: "blur(14px)",
    padding: "22px",
    borderRadius: "8px",
    boxShadow: "0 12px 32px rgba(0,0,0,0.45)"
  },
  field: {
    display: "flex",
    flexDirection: "column",
    marginBottom: "14px"
  },
  select: {
    padding: "10px 12px",
    borderRadius: "8px",
    border: "1px solid rgba(255,255,255,0.2)",
    background: "rgba(255,255,255,0.08)",
    color: "#ffffff",
    fontSize: "14px",
    outline: "none",
    cursor: "pointer"
  },
  button: {
    marginTop: "28px",
    width: "100%",
    padding: "15px",
    borderRadius: "8px",
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
    borderRadius: "8px",
    textAlign: "center"
  },
  error: {
    marginTop: "18px",
    padding: "14px",
    background: "rgba(255,107,107,0.18)",
    border: "1px solid rgba(255,107,107,0.45)",
    borderRadius: "8px"
  },
  warning: {
    margin: 0,
    padding: "14px",
    color: "#ffd166",
    background: "rgba(255,209,102,0.12)",
    borderRadius: "8px"
  },
  note: {
    fontSize: "13px",
    opacity: 0.75,
    marginTop: "8px"
  },
  explanationSection: {
    marginTop: "20px",
    padding: "16px",
    background: "rgba(0,0,0,0.2)",
    borderRadius: "8px"
  },
  tabs: {
    display: "flex",
    gap: "8px",
    marginBottom: "16px"
  },
  tab: {
    padding: "10px 16px",
    border: "none",
    borderRadius: "8px",
    fontSize: "14px",
    fontWeight: "600",
    cursor: "pointer"
  },
  tabActive: {
    background: "linear-gradient(135deg,#00b4db,#0083b0)",
    color: "#ffffff"
  },
  tabInactive: {
    background: "rgba(255,255,255,0.1)",
    color: "rgba(255,255,255,0.6)"
  },
  explanationContent: {
    marginTop: "12px"
  },
  baseValue: {
    fontSize: "14px",
    marginBottom: "12px",
    opacity: 0.9
  },
  features: {
    display: "flex",
    flexDirection: "column",
    gap: "10px"
  },
  featureRow: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "8px",
    background: "rgba(255,255,255,0.05)",
    borderRadius: "8px",
    fontSize: "13px"
  },
  featureName: {
    minWidth: "180px",
    fontWeight: "500",
    color: "#00d4a3",
    textAlign: "left"
  },
  bar: {
    flex: 1,
    height: "18px",
    background: "rgba(255,255,255,0.1)",
    borderRadius: "4px",
    overflow: "hidden"
  },
  barFill: {
    height: "100%",
    transition: "width 0.3s ease"
  },
  featureValue: {
    minWidth: "70px",
    textAlign: "right",
    fontWeight: "500",
    color: "#ffffff"
  }
};

export default App;
