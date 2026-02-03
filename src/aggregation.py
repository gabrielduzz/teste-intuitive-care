import pandas as pd
import zipfile

df = pd.read_csv('./data/processed/resultado_validado.csv', encoding='latin1')

df_aggregated = df.groupby(['Razao_Social', 'UF'])['ValorDespesas'].agg(['sum', 'mean', 'std'])

print(df_aggregated.head())

df_aggregated.columns = ['Total_Despesas', 'Media_Trimestral', 'Desvio_Padrao']

df_aggregated = df_aggregated.round(2)

df_aggregated = df_aggregated.sort_values(by='Total_Despesas', ascending=False)

df_final_aggregated = df_aggregated.reset_index()

csv_filename = "./data/processed/despesas_agregadas.csv"

df_final_aggregated.to_csv(csv_filename, index=False)

print("File 'despesas_agregadas.csv' saved successfully!")
print(df_final_aggregated.head())

zip_filename = "./data/processed/Teste_Gabriel_dos_Santos.zip"

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_filename)

print(f"File {zip_filename} compacted!")