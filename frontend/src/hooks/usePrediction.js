import { useState } from "react";
import { postJson } from "../api/apiClient";

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

export function usePrediction() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [shap, setShap] = useState(null);
  const [lime, setLime] = useState(null);
  const [error, setError] = useState("");
  const [shapError, setShapError] = useState("");
  const [limeError, setLimeError] = useState("");
  const [loading, setLoading] = useState(false);

  const updateForm = (key, value) => {
    setForm((current) => ({ ...current, [key]: value }));
  };

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

  return {
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
  };
}
