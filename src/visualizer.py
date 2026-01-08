import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Set visual standards for scientific reporting
sns.set_theme(style="whitegrid")
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def plot_subject_status(df: pd.DataFrame, output_path: str = "results/partial_status.png"):
    """
    Visualizes student status distribution across subjects.
    Provides a clear diagnostic for interdisciplinary management.
    """
    try:
        plt.figure(figsize=(12, 7))
        
        # Consistent color mapping for pedagogical outcomes
        color_map = {
            'Aprovado': '#2ca02c',      # Success
            'Exame Final': '#ff7f0e',   # Warning
            'Retido (Nota)': '#d62728'  # Critical
        }
        
        ax = sns.countplot(
            data=df,
            x='Subject',
            hue='Res. Parcial',
            palette=color_map
        )
        
        plt.title('Academic Status Distribution per Subject', fontsize=16, weight='bold')
        plt.xlabel('Subject Area', fontsize=12)
        plt.ylabel('Student Count', fontsize=12)
        
        # Statistical annotation: Adding counts and percentages to bars
        total_records = len(df['Nome'].unique())
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                percentage = 100 * height / total_records
                ax.text(p.get_x() + p.get_width()/2., height + 0.1, 
                        f'{height:.0f}\n({percentage:.1f}%)', 
                        ha="center", fontsize=9, weight='bold')

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        logging.info(f"Analysis plot successfully exported to {output_path}")
        
    except Exception as e:
        logging.error(f"Visualization error (Status Plot): {e}")

def plot_grade_distribution(df: pd.DataFrame, output_path: str = "results/grade_distribution.png"):
    """
    Generates density histograms to analyze the performance spread.
    Essential for monitoring teaching quality and learning consistency.
    """
    try:
        subjects = df['Subject'].unique()
        fig, axes = plt.subplots(1, len(subjects), figsize=(20, 6), sharey=True)
        fig.suptitle('Interdisciplinary Grade Distribution Analysis', fontsize=18, weight='bold')

        for i, subject in enumerate(subjects):
            subset = df[df['Subject'] == subject]
            sns.histplot(data=subset, x='Média Final', ax=axes[i], 
                         binwidth=1, binrange=(0, 11), kde=True, color='skyblue')
            axes[i].set_title(subject, fontsize=14, weight='bold')
            axes[i].set_xticks(range(11))
            axes[i].set_xlabel('Final Grade')

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        logging.info(f"Grade distribution analysis exported to {output_path}")
        
    except Exception as e:
        logging.error(f"Visualization error (Distribution Plot): {e}")