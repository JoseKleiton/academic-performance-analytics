import pandas as pd
import numpy as np

def classify_profile(row):
    """
    Translates quantitative data into qualitative pedagogical diagnostics.
    Provides detailed profiles to guide intervention strategies.
    """
    high_avg, low_avg, high_std = 7.0, 5.0, 1.5

    # 1. Critical cases (Failures detected)
    if row['Cont_REP'] > 0:
        return 'CRITICAL SITUATION: Student has failure(s) in the final assessment.'
    
    # 2. High performance (High average and consistent)
    elif row['Media'] >= high_avg and row['Desv_Pad'] < high_std:
        return 'HIGH PERFORMANCE: Solid and consistent results across all subject areas.'
    
    # 3. Inconsistent (Approved but high fluctuation)
    elif row['Media'] >= low_avg and row['Desv_Pad'] >= high_std:
        return 'INCONSISTENT PERFORMANCE: Approved, but with significant grade fluctuation.'
    
    # 4. Low average (Approved but at risk)
    elif row['Media'] < low_avg:
        return 'GENERAL DIFFICULTY: Approved with low average, requires reinforcement of core concepts.'
    
    # 5. Standard case
    else:
        return 'STANDARD PERFORMANCE: Approved within the expected normal range.'

def anonymize_students(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replaces real student names with generic IDs to comply with 
    privacy standards and research ethics (LGPD).
    """
    df = df.copy()
    # Mapping unique names to consistent IDs
    unique_names = df['Nome'].unique()
    mapping = {name: f"STUDENT_{i+1:03d}" for i, name in enumerate(unique_names)}
    
    df['Nome'] = df['Nome'].map(mapping)
    return df

def process_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """Handles type conversion for all grade columns for scientific consistency."""
    cols = ['3º B', '4º B', 'Média Semestral', 'Exame Final', 'Média Final']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def generate_final_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """
    Consolidates data into the final Ranking format with specific column order.
    Sorted by lowest score (Pont) to highlight students needing intervention.
    """
    # Pivot grades and results for interdisciplinary view
    grades = df.pivot(index='Nome', columns='Subject', values='Média Final')
    results = df.pivot(index='Nome', columns='Subject', values='Res. Final')
    
    # Joining and renaming subject-specific columns
    ranking = grades.join(results, lsuffix='_Fin', rsuffix='_Res').reset_index()
    
    column_mapping = {
        'Nome': 'Aluno',
        'Informatics_Fin': 'Fin_Inf', 'Informatics_Res': 'Res_Inf',
        'Logic_Fin': 'Fin_Log', 'Logic_Res': 'Res_Log',
        'Maintenance_Fin': 'Fin_Man', 'Maintenance_Res': 'Res_Man'
    }
    ranking = ranking.rename(columns=column_mapping)

    # Statistical Metrics calculation
    res_cols = ['Res_Inf', 'Res_Log', 'Res_Man']
    fin_cols = ['Fin_Inf', 'Fin_Log', 'Fin_Man']
    
    ranking['Cont_REP'] = (ranking[res_cols] == 'Retido (Nota)').sum(axis=1)
    ranking['Cont_APR'] = (ranking[res_cols] == 'Aprovado').sum(axis=1)
    ranking['Media'] = ranking[fin_cols].mean(axis=1).round(2)
    ranking['Desv_Pad'] = ranking[fin_cols].std(axis=1).round(2)
    
    # Scoring: (APR * 3) + (REP * -5)
    ranking['Pont'] = (ranking['Cont_APR'] * 3) + (ranking['Cont_REP'] * -5)
    
    # Applying the qualitative profile
    ranking['Perfil'] = ranking.apply(classify_profile, axis=1)
    
    # Final column ordering
    final_order = [
        'Aluno', 'Pont', 'Media', 'Desv_Pad', 'Cont_REP', 'Cont_APR', 
        'Fin_Inf', 'Res_Inf', 'Fin_Log', 'Res_Log', 'Fin_Man', 'Res_Man', 'Perfil'
    ]
    
    # Sorting by lowest score (Ascending)
    return ranking[final_order].sort_values(by='Pont', ascending=True)