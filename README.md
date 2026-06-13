## Loan-Approval-Engine
# ⚠ Academic Integrity Notice

This repository is shared publicly for learning and portfolio review.
Submitting this project (or any substantial part of it) as your own
academic work is a violation of academic integrity policies.

Original work by: Harsh Bhardwaj
# Loan Approval Engine

Loan Approval Engine is a full-stack machine learning project that predicts whether a loan application should be approved or rejected based on applicant details. The project focuses not only on accurate prediction but also on transparency and explainability, which are critical in financial decision-making systems.

The core idea behind this project is to move beyond traditional rule-based loan approval systems and use machine learning to make smarter decisions while clearly explaining *why* a particular decision was made.

## Project Overview

The system takes applicant information as input, processes it through a trained machine learning model, and returns a loan approval decision. To ensure trust in the model, explainability techniques are applied so that individual predictions can be interpreted.

The project includes:
- A machine learning model trained for loan approval prediction
- A FastAPI backend to serve predictions
- A React-based frontend for user interaction
- Explainability using SHAP and LIME for model interpretation

## Machine Learning Details

The model used in this project is **XGBoost**, a gradient boosting algorithm that builds decision trees sequentially. Each new tree attempts to minimize the loss function by correcting the errors of the previous trees using gradient and Hessian information, along with regularization to prevent overfitting.

To make the model interpretable:
- **SHAP (SHapley Additive exPlanations)** is used to understand global and local feature importance.
- **LIME (Local Interpretable Model-agnostic Explanations)** is used to explain individual predictions.

These techniques help answer an important question: *why was a particular loan approved or rejected?*

## Tech Stack

Backend:
- Python
- FastAPI
- XGBoost
- SHAP
- LIME

Frontend:
- React.js
- HTML
- CSS
- JavaScript

Libraries & Tools:
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- Uvicorn

## Project Structure

loan-approval-engine  
├── app  
│   ├── main.py  
│   ├── schemas.py  
│   └── utils.py  
├── frontend  
│   ├── public  
│   └── src  
├── mynotebook.ipynb  
├── lime_explanation.html  
├── requirements.txt  
└── README.md  

## How to Run the Project

Clone the repository:
bash:
git clone https://github.com/rituharsh9436/Loan-Approval-Engine.git
cd Loan-Approval-Engine

Install backend dependencies:
bash:
pip install -r requirements.txt

Run the backend server:
bash:
uvicorn app.main:app --reload


Run the frontend:
bash:
cd frontend
npm install
npm start
