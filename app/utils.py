import pandas as pd

def preprocess_input(data, feature_columns):
    df = pd.DataFrame([data])

    df['Total_Income'] = df['Applicant_Income'] + df['Coapplicant_Income']
    df['Loan_to_Income_Ratio'] = df['Loan_Amount'] / df['Total_Income']

    df = pd.get_dummies(df)

    df = df.reindex(columns=feature_columns, fill_value=0)
    return df
