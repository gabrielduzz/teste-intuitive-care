import pandas as pd
import os, glob

data_dir = './data/raw'
csv_files = glob.glob(os.path.join(data_dir, '*.csv'))

dfs = []

for file in csv_files:
    print(f"Processing {file} ...")

    filename = os.path.basename(file)
    try:
        quarter = int(filename[0])
    except Exception as e:
        print("Filename is not an integer")
        continue
        

    df = pd.read_csv(file, sep=';', encoding='utf-8', dtype={'CD_CONTA_CONTABIL' : str})
    
    df_expenses = df[df['CD_CONTA_CONTABIL'] == '41'].copy()

    df_expenses['DATA'] = pd.to_datetime(df_expenses['DATA'], dayfirst=True)
    df_expenses['Ano'] = df_expenses['DATA'].dt.year
    df_expenses['Trimestre'] = quarter

    df_expenses['ValorDespesas'] = df_expenses['VL_SALDO_FINAL'].astype(str).str.replace(',', '.').astype(float) 
    
    df_final = df_expenses[['REG_ANS', 'Trimestre', 'Ano', 'ValorDespesas']]

    dfs.append(df_final)

if dfs:
    consolidated = pd.concat(dfs, ignore_index=True)

    inconsistent_data = consolidated[consolidated['ValorDespesas'] <= 0]
    print(f"\nTotal inconsistent records (<= 0): {len(inconsistent_data)}")

    print("Consolidation successful!")
    print(consolidated.head())

    consolidated_cleaned = consolidated[consolidated['ValorDespesas'] > 0]

    consolidated_cleaned.to_csv("./data/processed/consolidado_despesas.csv", index=False)
else:
    print("No data found!")


