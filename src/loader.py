import pandas as pd

def fetch_data(url: str) -> pd.ExcelFile:
    """
    Consumes the spreadsheet from Google Sheets via URL.
    
    Args:
        url (str): The export URL for the spreadsheet.
    Returns:
        pd.ExcelFile: Object containing all loaded sheets.
    """
    try:
        return pd.ExcelFile(url)
    except Exception as e:
        # Rigorous error handling for connection issues
        raise ConnectionError(f"Failed to access the remote database: {e}")

def load_subjects(excel_file: pd.ExcelFile, subjects_config: dict) -> pd.DataFrame:
    """
    Reads the configured sheets and consolidates the initial data.
    
    Args:
        excel_file (pd.ExcelFile): The loaded Excel object.
        subjects_config (dict): Mapping of sheet names to subject names.
    Returns:
        pd.DataFrame: Consolidated and initially cleaned data.
    """
    dataframes = []
    
    for sheet_name, subject_name in subjects_config.items():
        # Skipping header rows as per your original spreadsheet logic
        df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=7, skipfooter=1)
        df['Subject'] = subject_name
        dataframes.append(df)
    
    # Consolidate and drop rows without student names (data integrity)
    consolidated_df = pd.concat(dataframes, ignore_index=True)
    return consolidated_df.dropna(subset=['Nome'])