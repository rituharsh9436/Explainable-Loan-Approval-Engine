import React from "react";
import styles from "./Select.module.css";

const Select = ({ label, value, options, onChange }) => (
  <div className={styles.field}>
    <label>{label}</label>
    <select
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className={styles.select}
    >
      {Object.entries(options).map(([key, labelText]) => (
        <option key={key} value={key} className={styles.option}>
          {labelText}
        </option>
      ))}
    </select>
  </div>
);

export default Select;
