import pandas as pd
import numpy as np

def prepare_input_record(record, feature_columns):
    """
    Takes a raw dictionary of applicant details from the form,
    applies the same feature engineering as training,
    and returns a DataFrame aligned with the model's expected 55 feature columns.
    """
    # Create DataFrame from the single input record
    df = pd.DataFrame([record])
    
    # 1. Clean Application Details
    if 'OCCUPATION_TYPE' in df.columns:
        df['OCCUPATION_TYPE'] = df['OCCUPATION_TYPE'].fillna('Unknown')
    else:
        df['OCCUPATION_TYPE'] = 'Unknown'
        
    # Convert user-friendly input fields into dataset-compatible fields
    # On the web form, we collect:
    #   AGE_YEARS (e.g. 35) -> convert to DAYS_BIRTH = -float(AGE_YEARS) * 365.25
    #   EMPLAYMENT_STATUS ("Employed" or "Unemployed")
    #   YEARS_EMPLOYED_INPUT (e.g. 5) -> convert to DAYS_EMPLOYED
    
    if 'AGE_YEARS' in df.columns:
        age_years = float(df.loc[0, 'AGE_YEARS'])
        days_birth = -int(age_years * 365.25)
    else:
        days_birth = -15000  # Default to ~41 years old if missing
        
    if 'EMPLAYMENT_STATUS' in df.columns and df.loc[0, 'EMPLAYMENT_STATUS'] == 'Unemployed':
        days_employed = 365243
    elif 'YEARS_EMPLOYED_INPUT' in df.columns:
        years_emp = float(df.loc[0, 'YEARS_EMPLOYED_INPUT'])
        days_employed = -int(years_emp * 365.25)
    else:
        days_employed = 365243  # Default to unemployed if missing
        
    # Standard feature calculations used by training:
    df['EMPLOYED'] = days_employed != 365243
    df['YEARS_EMPLOYED'] = max(-days_employed / 365.25, 0) if days_employed != 365243 else 0
    df['AGE'] = int(-days_birth / 365.25)
    
    # Financial ratios
    df['INCOME_EMPLOY_RATIO'] = df.apply(
        lambda row: row['AMT_INCOME_TOTAL'] / row['YEARS_EMPLOYED'] if row['YEARS_EMPLOYED'] > 0 else row['AMT_INCOME_TOTAL'],
        axis=1
    )
    
    # Clean up temporary/intermediate columns that aren't model features
    df.drop(columns=['DAYS_EMPLOYED', 'DAYS_BIRTH', 'AGE_YEARS', 'EMPLAYMENT_STATUS', 'YEARS_EMPLOYED_INPUT'], inplace=True, errors='ignore')
    
    # 2. Credit History Flags
    # For a new applicant, these are filled with 0 (or we can lookup if they have a history)
    # We set default values matching the training features.
    for col in ['STATUS_MAX', 'STATUS_MIN', 'STATUS_MEAN', 'STATUS_LAST', 'STATUS_TREND', 'NUM_LATE_MONTHS']:
        if col not in df.columns:
            df[col] = 0.0
            
    # 3. Categorical Encoding (One-Hot Encoding)
    # We identify all categorical features and convert them
    categorical_cols = ['CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 
                        'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 
                        'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'OCCUPATION_TYPE']
    
    # Ensure all categorical columns are in the dataframe
    for col in categorical_cols:
        if col not in df.columns:
            df[col] = 'Unknown'
            
    # Perform dummy encoding
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    df_encoded = df_encoded.astype(float)
    
    # Reindex to match the exact columns the model was trained on
    # Any column that is missing is filled with 0.0
    df_aligned = df_encoded.reindex(columns=feature_columns, fill_value=0.0)
    
    return df_aligned
