import os
import logging
import pandas as pd
from dotenv import load_dotenv

# Importing custom modules from the src package
from src.loader import fetch_data, load_subjects
from src.processor import process_raw_data, generate_final_ranking, anonymize_students
from src.visualizer import plot_status, plot_distributions

# 1. Environment and Logging Configuration
load_dotenv()
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s: %(message)s'
)

# Constants and Configuration from .env
URL = os.getenv("GOOGLE_SHEET_URL")
# Privacy Toggle: Default is False (show real names) if not specified in .env
ANONYMIZE = os.getenv("ANONYMIZE_DATA", "False").lower() == "true"

SUBJECT_MAPPING = {
    'Informática(B)': 'Informatics',
    'Lógica(B)': 'Logic',
    'Manutenção(B)': 'Maintenance'
}

def main():
    """
    Main orchestrator for the Academic Performance Analytics tool.
    Coordinates the ETL pipeline with conditional privacy and data source fallback.
    """
    logging.info("Initializing Academic Performance Analysis pipeline...")
    os.makedirs("results", exist_ok=True)

    # 2. Data Source Selection (Remote vs Local Fallback)
    if URL:
        logging.info("Data Source: Remote Google Sheets (Production Mode)")
        try:
            data_source = fetch_data(URL)
        except Exception as e:
            logging.error(f"Failed to fetch remote data: {e}")
            return
    else:
        local_mock_path = "data/sample_data.xlsx"
        if os.path.exists(local_mock_path):
            logging.info(f"Data Source: Local Mock Data (Reproducibility Mode) -> {local_mock_path}")
            data_source = pd.ExcelFile(local_mock_path)
        else:
            logging.error("No data source found. Provide GOOGLE_SHEET_URL in .env or create data/sample_data.xlsx")
            return

    try:
        # 3. Ingestion and Technical Cleaning
        logging.info("Consolidating subject sheets and cleaning raw data...")
        raw_df = load_subjects(data_source, SUBJECT_MAPPING)
        processed_data = process_raw_data(raw_df)

        # 4. Conditional Privacy Layer (The Toggle)
        # Based on ANONYMIZE_DATA in your .env file
        if ANONYMIZE:
            logging.info("Privacy Mode: ON. Applying data anonymization for public reporting...")
            final_data = anonymize_students(processed_data)
        else:
            logging.info("Privacy Mode: OFF. Using real student names for pedagogical diagnostic...")
            final_data = processed_data.copy()

        # 5. Scientific Visualization (using the chosen data mode)
        logging.info("Generating visual diagnostic reports...")
        
        # 5.1 Partial Status Distribution
        plot_status(final_data, 'Res. Parcial', 'Partial Status Diagnostic', 'results/1_partial_status.png')
        
        # 5.2 Final Grade Distribution Histograms
        plot_distributions(final_data, 'Média Final', 'Final Grade Distribution', 'results/2_grades_hist.png', 'skyblue')
        
        # 5.3 Final Status Distribution (Post-Recovery)
        plot_status(final_data, 'Res. Final', 'Final Outcome Status', 'results/3_final_status.png')
        
        # 5.4 Recovery Performance Analysis
        recovery_subset = final_data[final_data['Res. Parcial'] == 'Exame Final']
        if not recovery_subset.empty:
            plot_distributions(recovery_subset, 'Exame Final', 'Recovery Exam Performance', 'results/4_recovery_hist.png', 'salmon')

        # 6. Statistical Consolidation and Performance Ranking
        logging.info("Calculating final performance ranking and qualitative profiles...")
        final_ranking = generate_final_ranking(final_data)
        
        # Exporting the consolidated report
        final_ranking.to_csv("results/final_ranking.csv", index=False)
        
        # Console output Summary
        print("\n" + "="*80)
        print("PIPELINE EXECUTION SUMMARY")
        print("="*80)
        print(f"Privacy Mode: {'ENABLED (Anonymized)' if ANONYMIZE else 'DISABLED (Real Names)'}")
        print(f"Total Students Processed: {len(final_ranking)}")
        print("-" * 80)
        # Print top 10 (sorted by lowest score as requested)
        print(final_ranking[['Aluno', 'Pont', 'Media', 'Perfil']].head(10).to_string(index=False))
        print("="*80)
        
        logging.info("Pipeline executed successfully. Files saved in 'results/'.")

    except Exception as e:
        logging.error(f"Critical pipeline failure: {e}")

if __name__ == "__main__":
    main()