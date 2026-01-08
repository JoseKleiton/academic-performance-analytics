# Academic Performance Analytics: Data-Driven Pedagogical Diagnostics

## 1. Project Overview
This software is an automated analytical tool designed to enhance academic management through data-driven diagnostics. By integrating raw educational data with statistical modeling, the system identifies student performance patterns and provides visual insights to support pedagogical interventions in interdisciplinary contexts.

## 2. Core Features
* **Automated ETL Pipeline**: Consumes data directly from cloud sources (Google Sheets) using Python-based extraction modules.
* **Statistical Profiling**: Implements rigorous data cleaning and metrics calculation, including global averages and standard deviations to assess learning consistency.
* **Diagnostic Visualization**: Generates high-impact charts to communicate scientific information to diverse audiences, from faculty to administrative coordinators.
* **Custom Performance Ranking**: Utilizes a weighted scoring system to prioritize pedagogical support based on final outcomes:
    $$Score = (\text{Approvals} \times 3) + (\text{Final Failures} \times -5)$$

## 3. Methodology & Rigor
This project implements research software engineering standards to ensure the validity and reliability of the generated insights:
* **Data Integrity & Normalization**: Automated handling of missing values (NaN) and strict type coercion for numeric fields (grades, final exams) to prevent calculation errors during the aggregation process.
* **Pedagogical Modeling**: Beyond basic grade reporting, the system calculates the **Standard Deviation** across interdisciplinary subjects to identify cases of inconsistent performance or specific learning gaps.
* **Modular Orchestration**: The separation of concerns between data ingestion, statistical processing, and visualization ensures that the analytical pipeline remains scalable and maintainable for different academic periods.
* **Traceable Execution**: Implementation of structured logging and exception handling to monitor the pipeline's health and ensure successful diagnostic exports.

## 4. Project Structure
```text
academic-performance-analytics/
├── data/               # Local data storage (e.g., mock data for testing)
├── notebooks/          # Exploratory Data Analysis (EDA) and prototyping
├── src/                # Modular source code
│   ├── loader.py       # Data ingestion (ETL) and Google Sheets integration
│   ├── processor.py    # Statistical logic and pedagogical profiling
│   └── visualizer.py   # Scientific reporting engine and plot generation
├── main.py             # Pipeline orchestrator and main entry point
└── requirements.txt    # Project dependencies and environment specification
```
## 5. Installation and Usage
1. Clone the repository: git clone https://github.com/your-username/academic-performance-analytics.git

2. Install dependencies: pip install -r requirements.txt

3. Run the analytical pipeline: python main.py