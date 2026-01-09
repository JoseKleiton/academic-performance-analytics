# Academic Performance Analytics: Interdisciplinary Pedagogical Diagnostics

## 1. Project Overview
This software is an automated analytical system designed to enhance academic management through data-driven diagnostics. By integrating raw educational data with statistical modeling, the system identifies student performance patterns and provides visual insights to support pedagogical interventions. The tool follows the **CRISP-DM** (Cross-Industry Standard Process for Data Mining) methodology to ensure scientific rigor and traceable execution.



## 2. Core Features
* **Modular ETL Pipeline**: Complete separation of concerns between data ingestion (`loader.py`), statistical processing (`processor.py`), and scientific visualization (`visualizer.py`).
* **Ethical Data Handling (LGPD)**: Built-in privacy layer allowing for the anonymization of student names via a conditional toggle (`ANONYMIZE_DATA`) in the environment settings.
* **Weighted Scoring System**: Implements a custom formula to prioritize pedagogical intervention based on interdisciplinary results: 
    $$Score = (\text{Approvals} \times 3) + (\text{Final Failures} \times -5)$$
* **Qualitative Profiling**: Automatically categorizes students into five distinct profiles (e.g., "High Performance", "Critical Situation", "Inconsistent") based on mean grades and standard deviation thresholds (7.0, 5.0, and 1.5).
* **Automated Scientific Reporting**: Generates four distinct diagnostic plots with automated annotations, absolute counts, and percentage distributions.

## 3. Methodology: CRISP-DM Workflow
The analytical pipeline is documented and executed through six iterative phases:

1.  **Business Understanding**: Defining diagnostic goals and qualitative profiling heuristics.
2.  **Data Understanding**: Consuming disciplinary data while skipping administrative spreadsheet headers (7 rows).
3.  **Data Preparation**: Automated technical cleaning, type coercion for numeric consistency, and conditional name masking.
4.  **Modeling**: Applying statistical calculations to generate the interdisciplinary ranking and scoring.
5.  **Evaluation**: Validating heuristics through comparative visual reports (pre and post-recovery).
6.  **Deployment**: Exporting consolidated CSV rankings and PNG diagnostic charts to the `results/` directory.

## 4. Project Structure
```text
academic-performance-analytics/
├── data/               # Local data storage (sample_data.xlsx)
├── notebooks/          # CRISP-DM Interactive Documentation (academic_analysis.ipynb)
├── results/            # Automated Diagnostic Exports (Charts and CSV)
├── scripts/            # Utility scripts for data generation and testing
├── src/                # Modular Source Code
│   ├── loader.py       # Data ingestion (ETL) and sheet consolidation
│   ├── processor.py    # Statistical logic and qualitative profiling
│   └── visualizer.py   # Scientific reporting engine (Seaborn/Matplotlib)
├── .env                # Environment variables (URL and Privacy toggles)
├── main.py             # Pipeline orchestrator and entry point
└── requirements.txt    # Project dependencies and version specifications
```

## 5. Installation and Usage
**Prerequisites**
* Python 3.10+: The core language used for all analytical modules.

**1. Environment Setup**
Clone the repository and install the project dependencies:

``` Bash
git clone https://github.com/your-username/academic-performance-analytics.git
cd academic-performance-analytics
pip install -r requirements.txt
```
**2. Configuration**
The pipeline uses an environment file for secure configuration. Create a .env file in the project root with the following parameters:

* GOOGLE_SHEET_URL: The full URL of your source spreadsheet.

* ANONYMIZE_DATA: Set to True to enable LGPD-compliant name masking or False to use real student names.

**3. Execution**
You can run the analytics through the command-line orchestrator or the interactive notebook:

* **Terminal**: Execute python main.py to trigger the full ETL and reporting pipeline.

* **Jupyter**: Open: Open notebooks/academic_analysis.ipynb to follow the step-by-step CRISP-DM interactive documentation.

**6. Scientific Visualization Suite**
The system automatically generates four diagnostic reports in the results/ directory to facilitate pedagogical review:

* 1_partial_status.png: Distribution of student status (Approved, Final Exam, Failed) before the recovery period.

* 2_grades_hist.png: Multi-disciplinary grade density analysis using histograms and Kernel Density Estimation (KDE) to identify performance distribution patterns.

* 3_final_status.png: Final academic outcomes across all subjects after the incorporation of recovery exam results.

* 4_recovery_hist.png: Targeted performance analysis specifically for the student population that required the Final Exam.