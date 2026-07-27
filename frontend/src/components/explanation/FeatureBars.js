import React from "react";
import styles from "./FeatureBars.module.css";

const FeatureBars = ({ features }) => (
  <div className={styles.features}>
    {Object.entries(features)
      .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
      .slice(0, 10)
      .map(([feature, value]) => (
        <div key={feature} className={styles.featureRow}>
          <span className={styles.featureName}>{feature}</span>
          <div className={styles.bar}>
            <div
              className={styles.barFill}
              style={{
                width: `${Math.min(Math.abs(value) * 100, 100)}%`,
                background: value > 0 ? "#00d4a3" : "#ff6b6b"
              }}
            />
          </div>
          <span className={styles.featureValue}>{Number(value).toFixed(4)}</span>
        </div>
      ))}
  </div>
);

export default FeatureBars;
