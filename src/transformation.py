import pandas as pd
import requests, os

base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
filename = "Relatorio_cadop.csv"
complete_url = base_url + filename
dest_path = os.path.join("./data/raw/", filename)

if not os.path.exists(dest_path):
    print(f"Downloading {filename}...")
    
    try:
        r = requests.get(complete_url)
        r.raise_for_status()

        with open(dest_path, 'wb') as f:
            f.write(r.content)
        
        print("Download finished!")
    except Exception as e:  
        print(f"Download unsuccesful: {e}")
else:
    print(f"File {filename} already exists in ./data. Skipping download.")

print("\nInspecting columns")
try:
    df_cadop = pd.read_csv(dest_path, sep=';', encoding='latin-1')

    print("Columns found:")
    print(df_cadop.columns.tolist())

    print("First line of data:")
    print(df_cadop.head(1))

except Exception as e:
    print(f"Error while reading CSV: {e}")
