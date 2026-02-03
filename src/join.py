import pandas as pd
import os

consolidated = pd.read_csv("./data/processed/consolidado_despesas.csv")
cadop = pd.read_csv("./data/raw/Relatorio_cadop.csv", sep=';', encoding='latin1', dtype={'CNPJ': str})

print("Data loaded!")
print(f"Consolidated: {consolidated.shape}")
print(f"Cadop: {cadop.shape}")

df_merged = pd.merge(consolidated, cadop, how='left', left_on='REG_ANS', right_on='REGISTRO_OPERADORA')

print("Columns after merge: ", df_merged.columns) 

columns_to_keep = ['CNPJ', 'Razao_Social', 'Trimestre', 'Ano', 'ValorDespesas', 'REG_ANS', 'Modalidade', 'UF']
df_final = df_merged[columns_to_keep]
df_final.rename(columns={
    'REG_ANS': 'RegistroANS'          
}, inplace=True)

output_file = "./data/processed/consolidado_enriquecido.csv"
df_final.to_csv(output_file, index=False, encoding='latin1')

print(f"File '{output_file}' saved successfully!")
print("Final columns: ", df_final.columns.tolist()) 