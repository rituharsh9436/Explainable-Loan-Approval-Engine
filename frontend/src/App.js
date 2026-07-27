import React, { useEffect } from "react";
import LoanForm from "./components/form/LoanForm";
import ExplanationResult from "./components/explanation/ExplanationResult";
import { usePrediction } from "./hooks/usePrediction";
import styles from "./App.module.css";

function App() {
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

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <header className={styles.header}>
          <h1>Loan Approval Engine</h1>
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

export default App;
