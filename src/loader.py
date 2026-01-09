import pandas as pd

def fetch_data(url: str) -> pd.ExcelFile:
    """Consumes the spreadsheet from Google Sheets."""
    try:
        return pd.ExcelFile(url)
    except Exception as e:
        raise ConnectionError(f"Failed to access database: {e}")

def load_subjects(excel_file: pd.ExcelFile, subjects_config: dict) -> pd.DataFrame:
    """Loads, cleans initially, and consolidates all subject sheets."""
    dataframes = []
    for sheet_name, subject_name in subjects_config.items():
        # skipping rows as per original logic
        df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=7, skipfooter=1)
        df['Subject'] = subject_name
        dataframes.append(df)
    
    # Cleaning: dropping rows without student names
    return pd.concat(dataframes, ignore_index=True).dropna(subset=['Nome'])