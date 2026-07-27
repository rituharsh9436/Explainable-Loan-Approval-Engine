import React, { useState } from "react";
import FeatureBars from "./FeatureBars";
import { API_BASE_URL } from "../../api/apiClient";
import styles from "./ExplanationResult.module.css";

const ExplanationMessage = ({ error, children }) => {
  if (error) {
    return <p className={styles.warning}>{error}</p>;
  }
  return children || <p className={styles.warning}>Click on LIME Explanation.</p>;
};

const ExplanationResult = ({ result, shap, lime, shapError, limeError }) => {
  const [explanationTab, setExplanationTab] = useState("shap");

  if (!result) return null;

  return (
    <div className={styles.result}>
      <h2 style={{ color: result.decision === "Approved" ? "#00d4a3" : "#ff6b6b" }}>
        {result.decision}
      </h2>
      <p>
        Approval Probability: <strong>{result.approval_probability}</strong>
      </p>

      <div className={styles.explanationSection}>
        <div className={styles.tabs}>
          <button
            className={`${styles.tab} ${
              explanationTab === "shap" ? styles.tabActive : styles.tabInactive
            }`}
            onClick={() => setExplanationTab("shap")}
          >
            SHAP Explanation
          </button>
          <button
            className={`${styles.tab} ${
              explanationTab === "lime" ? styles.tabActive : styles.tabInactive
            }`}
            onClick={() => {
              setExplanationTab("lime");
              window.open(`${API_BASE_URL}/api/v1/lime-report`, "_blank");
            }}
          >
            LIME Explanation
          </button>
        </div>

        {explanationTab === "shap" && (
          <ExplanationMessage error={shapError}>
            {shap?.shap_values && (
              <div className={styles.explanationContent}>
                <h3>SHAP Feature Contributions</h3>
                <p className={styles.baseValue}>
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
              <div className={styles.explanationContent}>
                <h3>LIME Local Explanations</h3>
                <div className={styles.features}>
                  {Object.entries(lime.lime_features).map(([feature, value]) => (
                    <div key={feature} className={styles.featureRow}>
                      <span className={styles.featureName}>{feature}</span>
                      <span className={styles.featureValue}>{Number(value).toFixed(4)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </ExplanationMessage>
        )}
      </div>

      <p className={styles.note}>
        Decision supported by model explainability and feature-level contribution analysis.
      </p>
    </div>
  );
};

export default ExplanationResult;
