import React from "react";
import Card from "../ui/Card";
import Slider from "../ui/Slider";
import Select from "../ui/Select";
import styles from "./LoanForm.module.css";

const LoanForm = ({ form, update }) => {
  return (
    <div className={styles.grid}>
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
  );
};

export default LoanForm;
