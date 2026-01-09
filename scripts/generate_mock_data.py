import pandas as pd
import numpy as np
import os

def create_mock_excel():
    """
    Generates a synthetic dataset of 30 students covering all pedagogical profiles:
    Critical, High Performance, Inconsistent, Low Average, and Standard.
    """
    os.makedirs("data", exist_ok=True)
    file_path = "data/sample_data.xlsx"
    
    students = [
        "Maria Silva", "José Oliveira", "Ana Santos", "João Souza", "Antônio Ferreira",
        "Francisca Pereira", "Carlos Rodrigues", "Paulo Almeida", "Lucas Nascimento", "Maria Oliveira",
        "Gabriel Alves", "Juliana Lima", "Letícia Carvalho", "Beatriz Gomes", "Marcos Rocha",
        "Fernanda Costa", "Patrícia Ribeiro", "Amanda Martins", "Rafael Barbosa", "Bruno Freitas",
        "Sérgio Melo", "Ricardo Cardoso", "Daniela Teixeira", "Vanessa Cavalcanti", "Thiago Barros",
        "Aline Guimarães", "Renato Machado", "Camila Castro", "Felipe Vieira", "Rodrigo Cunha"
    ]

    subjects = ['Informática(B)', 'Lógica(B)', 'Manutenção(B)']
    all_data = {s: [] for s in subjects}

    for i, name in enumerate(students):
        # Strategic profile assignment for testing
        if i == 0:    # Critical: Direct failure
            grades = [2.0, 2.5, 2.0]
        elif i == 1:  # High Performance: High and consistent
            grades = [9.5, 9.8, 9.6]
        elif i == 2:  # Inconsistent: High average but high fluctuation
            grades = [10.0, 4.0, 7.0] 
        elif i == 3:  # Low Average: Average < 5.0 without immediate failure
            grades = [4.8, 4.7, 4.9] 
        elif i == 4:  # Standard: Performance between 5.0 and 7.0
            grades = [6.5, 6.0, 6.2]
        else:         # General distribution for data volume
            if i % 3 == 0:   grades = [7.0, 7.5, 7.2]
            elif i % 3 == 1: grades = [5.5, 8.0, 6.0]
            else:            grades = [4.0, 5.0, 5.5]

        for s_idx, s_name in enumerate(subjects):
            semester_avg = grades[s_idx]
            
            # Logic to ensure data for Recovery Analysis (Plot 4)
            needs_recovery = 3.0 <= semester_avg < 6.0
            final_exam = semester_avg + 2.0 if needs_recovery else (0.0 if semester_avg < 3.0 else np.nan)
            
            # Final Average Calculation
            if not np.isnan(final_exam) and final_exam > 0:
                final_avg = (semester_avg + final_exam) / 2
            else:
                final_avg = semester_avg

            # Academic status strings based on original template
            partial_res = 'Exame Final' if needs_recovery else ('Retido (Nota)' if semester_avg < 3.0 else 'Aprovado')
            final_res = 'Aprovado' if final_avg >= 5.0 else 'Retido (Nota)'

            all_data[s_name].append({
                'Nome': name,
                '3º B': semester_avg, 
                '4º B': semester_avg,
                'Média Semestral': semester_avg,
                'Exame Final': final_exam,
                'Média Final': round(final_avg, 2),
                'Res. Parcial': partial_res,
                'Res. Final': final_res
            })

    # Writing to Excel with row offset to match pedagogical template
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for s_name in subjects:
            df = pd.DataFrame(all_data[s_name])
            df.to_excel(writer, sheet_name=s_name, startrow=7, index=False)

    print(f"Mock data successfully generated at: {file_path}")
    print("Profile coverage: Critical, High, Inconsistent, Low Avg, and Standard.")

if __name__ == "__main__":
    create_mock_excel()