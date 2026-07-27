import React from "react";
import styles from "./Slider.module.css";

const Slider = ({ label, value, min, max, step, unit, onChange }) => (
  <div className={styles.field}>
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

export default Slider;
