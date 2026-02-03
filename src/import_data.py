import pandas as pd
from sqlalchemy import create_engine
from datetime import date

connection_string = 'postgresql://user_teste:password_teste@localhost:5432/ans_database'
engine = create_engine(connection_string)

print("Connecting to database...")

df = pd.read_csv('./data/processed/resultado_validado.csv', encoding='latin1')

print("Preparing data from companies...")

df_companies = df[['RegistroANS', 'CNPJ', 'Razao_Social', 'Modalidade', 'UF']].drop_duplicates(subset=['RegistroANS'])

df_companies = df_companies.rename(columns={
    'RegistroANS': 'ans_id',
    'CNPJ': 'cnpj',
    'Razao_Social': 'company_name',
    'Modalidade': 'modality',
    'UF': 'state'
})

try:
    df_companies.to_sql('dim_companies', engine, if_exists='append', index=False)
    print(f"Success! {len(df_companies)} companies imported.")
except Exception as e:
    print(f"Error while importing companies: {e}")

print("Preparing expenses data...")

df_expenses = df[['RegistroANS', 'Ano', 'Trimestre', 'ValorDespesas']].copy()

df_expenses = df_expenses.rename(columns={
    'RegistroANS': 'ans_id',
    'Ano': 'year',
    'Trimestre': 'quarter',
    'ValorDespesas': 'amount'
})

df_expenses['reference_date'] = df_expenses.apply(
    lambda row: date(int(row['year']), int(row['quarter'])*3 - 2, 1), axis=1
)

try:
    df_expenses.to_sql('fact_expenses', engine, if_exists='append', index=False)
    print(f"Success! {len(df_expenses)} expenses records imported.")
except Exception as e:
    print(f"Error while importing expenses: {e}")

