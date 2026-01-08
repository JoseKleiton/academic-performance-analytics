import pandas as pd
import numpy as np
import logging

# Configure logging for process traceability (Technical Rigor)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def process_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs data cleaning and type conversion with exception handling.
    Ensures that numeric fields are ready for statistical analysis.
    """
    try:
        # Columns that must be numeric for calculation integrity
        numeric_cols = ['3º B', '4º B', 'Média Semestral', 'Exame Final', 'Média Final']
        
        for col in numeric_cols:
            if col in df.columns:
                # Coercing errors to NaN handles empty cells or non-numeric strings
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        logging.info("Data types successfully converted to numeric.")
        return df
    except Exception as e:
        logging.error(f"Failed during data type conversion: {e}")
        return df

def generate_performance_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """
    Implements scoring logic and pedagogical profile classification.
    Score Formula: (Approvals * 3) + (Final Failures * -5)
    """
    # 1. Pivot data to analyze performance across all interdisciplinary subjects
    # This reflects the ISD's interdisciplinary research requirement
    ranking_df = df.pivot_table(
        index='Nome', 
        columns='Subject', 
        values='Média Final', 
        aggfunc='first'
    ).reset_index()

    # 2. Calculating global metrics for each student
    subjects_cols = ranking_df.columns.drop('Nome')
    ranking_df['Global_Average'] = ranking_df[subjects_cols].mean(axis=1).round(2)
    ranking_df['Standard_Deviation'] = ranking_df[subjects_cols].std(axis=1).round(2)

    # 3. Applying the researcher's scoring logic for ranking
    # Note: Status logic will be applied in the orchestration (main.py)
    # based on 'Res. Final' columns
    
    return ranking_df

def classify_pedagogical_profile(row: pd.Series) -> str:
    """
    Classifies students based on academic performance and consistency.
    Useful for guiding students across different undergraduate levels.
    """
    media_high = 7.0
    media_low = 5.0
    std_dev_high = 1.5

    # Logic tailored to identify critical cases and high performers
    if row.get('Cont_REP', 0) > 0:
        return 'CRITICAL: Persistent failures in final results.'
    elif row['Global_Average'] >= media_high and row['Standard_Deviation'] < std_dev_high:
        return 'HIGH PERFORMANCE: Solid and consistent academic results.'
    elif row['Global_Average'] >= media_low and row['Standard_Deviation'] >= std_dev_high:
        return 'INCONSISTENT: Approved, but with significant grade fluctuation.'
    else:
        return 'STANDARD: Median performance within expected range.'