import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def plot_status(df: pd.DataFrame, col: str, title: str, path: str):
    """
    Plots status distribution with absolute counts, percentages, and semantic colors.
    """
    try:
        plt.figure(figsize=(12, 7))
        
        status_colors = {
            'Aprovado': '#2ca02c',      # Green
            'Exame Final': '#ff7f0e',   # Orange
            'Retido (Nota)': '#d62728'  # Red
        }
        
        ax = sns.countplot(data=df, x='Subject', hue=col, palette=status_colors)
        
        plt.title(title, weight='bold', fontsize=16)
        plt.xlabel('Subject', fontsize=12)
        plt.ylabel('Student Count', fontsize=12)
        plt.legend(title=col, bbox_to_anchor=(1.05, 1), loc='upper left')

        # Annotations for Status Plot
        total_students = len(df['Nome'].unique())
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                percentage = 100 * height / total_students
                ax.text(
                    p.get_x() + p.get_width()/2., 
                    height + 0.1, 
                    f'{height:.0f}\n({percentage:.1f}%)', 
                    ha="center", fontsize=9, weight='bold'
                )

        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        logging.info(f"Successfully saved annotated status plot: {path}")
    except Exception as e:
        logging.error(f"Error generating status plot: {e}")

def plot_distributions(df: pd.DataFrame, col: str, title: str, path: str, color: str):
    """
    Plots histograms for grade distributions with count and percentage labels.
    Provides precise frequency analysis for pedagogical assessment.
    """
    try:
        subjects = df['Subject'].unique()
        if len(subjects) == 0:
            return

        fig, axes = plt.subplots(1, len(subjects), figsize=(20, 7), sharey=True)
        fig.suptitle(title, weight='bold', fontsize=18)
        
        if len(subjects) == 1:
            axes = [axes]

        for i, s in enumerate(subjects):
            subset = df[df['Subject'] == s]
            total_in_subset = len(subset)
            
            # Generating the histogram
            ax_sub = sns.histplot(
                subset[col], 
                ax=axes[i], 
                binwidth=1, 
                binrange=(0,11), 
                kde=True, 
                color=color
            )
            
            axes[i].set_title(f"{s}\n(Total: {total_in_subset})", weight='semibold', fontsize=14)
            axes[i].set_xticks(range(11))
            axes[i].set_xlabel('Grade')
            
            # Annotations for Histogram Bins
            # Each 'p' is a bar representing a grade interval
            for p in axes[i].patches:
                height = p.get_height()
                if height > 0:
                    percentage = 100 * height / total_in_subset
                    axes[i].text(
                        p.get_x() + p.get_width()/2., 
                        height + 0.05, 
                        f'{height:.0f}\n({percentage:.1f}%)', 
                        ha="center", 
                        va="bottom",
                        fontsize=8, 
                        weight='bold',
                        color='black'
                    )

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(path)
        plt.close()
        logging.info(f"Successfully saved annotated distribution: {path}")
    except Exception as e:
        logging.error(f"Error generating distribution plot: {e}")