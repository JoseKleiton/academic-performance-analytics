import os
import logging
import pandas as pd
from src.loader import fetch_data, load_subjects
from src.processor import process_raw_data, generate_performance_ranking
from src.visualizer import plot_subject_status, plot_grade_distribution

# 1. Configuration Constants (Separation of concerns)
SHEET_ID = "1_KfhUlmBFatxUmjTmeszD4OJ-VwBQMQnGQjioMacNUk"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

# Mapping sheets to their respective international subject names
SUBJECT_MAPPING = {
    'Informática(B)': 'Informatics',
    'Lógica(B)': 'Logic',
    'Manutenção(B)': 'Maintenance'
}

# 2. Setup Logging for traceability
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    """
    Main entry point for the Academic Performance Analytics tool.
    Coordinates the ETL pipeline, statistical analysis, and visualization.
    """
    logging.info("Starting Academic Performance Analysis pipeline...")

    # Step 0: Environment Setup (Ensuring required directories exist)
    os.makedirs("results", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    try:
        # Step 1: Data Ingestion
        # Connects to the remote source and loads raw data
        logging.info("Fetching data from remote source...")
        excel_file = fetch_data(BASE_URL)
        raw_df = load_subjects(excel_file, SUBJECT_MAPPING)

        # Step 2: Data Processing & Cleaning
        # Ensures scientific rigor by handling missing values and data types
        logging.info("Cleaning raw data and processing metrics...")
        cleaned_df = process_raw_data(raw_df)
        
        # Step 3: Visualization & Diagnostic Reporting
        # Generates high-impact charts for pedagogical support
        logging.info("Generating visual diagnostic reports...")
        plot_subject_status(cleaned_df, output_path="results/status_distribution.png")
        plot_grade_distribution(cleaned_df, output_path="results/grade_distribution.png")

        # Step 4: Statistical Ranking & Export
        # Consolidates student performance for final assessment
        logging.info("Calculating final performance ranking...")
        ranking_results = generate_performance_ranking(cleaned_df)
        
        # Exporting clean data for reproducibility
        ranking_results.to_csv("results/academic_ranking.csv", index=False)
        
        logging.info("Pipeline executed successfully. Reports are available in the 'results/' folder.")

    except Exception as e:
        # Critical error management to prevent silent failures
        logging.error(f"Critical failure during execution: {e}")

if __name__ == "__main__":
    main()