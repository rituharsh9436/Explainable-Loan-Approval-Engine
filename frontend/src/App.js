import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import LoanForm from "./components/form/LoanForm";
import ExplanationResult from "./components/explanation/ExplanationResult";
import { usePrediction } from "./hooks/usePrediction";
import { AuthProvider, useAuth } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import styles from "./App.module.css";

function Dashboard() {
  useEffect(() => {
    document.title = "Loan Approval Engine";
  }, []);

  const {
    form,
    updateForm,
    result,
    shap,
    lime,
    error,
    shapError,
    limeError,
    loading,
    predict
  } = usePrediction();

  const { logout } = useAuth();
  
  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <header className={styles.header}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h1>Loan Approval Engine</h1>
            <button onClick={logout} className={styles.button} style={{ width: 'auto', padding: '8px 16px', background: '#e74c3c' }}>Logout</button>
          </div>
          <p>
            A transparent machine learning system for credit risk assessment
            with interpretable decisions and consistent feature analysis.
            Using XGBoost with SHAP and LIME explanations.
          </p>
        </header>

        <LoanForm form={form} update={updateForm} />

        <button className={styles.button} onClick={predict} disabled={loading}>
          {loading ? "Evaluating application..." : "Evaluate Loan Application"}
        </button>

        {error && <div className={styles.error}>{error}</div>}

        <ExplanationResult
          result={result}
          shap={shap}
          lime={lime}
          shapError={shapError}
          limeError={limeError}
        />
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route 
            path="/" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
