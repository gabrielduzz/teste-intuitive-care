import pandas as pd

first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
second_weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

def calculate_first_digit(base):
    base_sum = sum(int(digit) * weight for digit, weight in zip(base, first_weights))

    remainder = base_sum % 11

    first_digit = 0 if remainder < 2 else 11 - remainder

    return str(first_digit)

def calculate_second_digit(base):
    base_sum = sum(int(digit) * weight for digit, weight in zip(base, second_weights))

    remainder = base_sum % 11

    second_digit = 0 if remainder < 2 else 11 - remainder

    return str(second_digit)

def validate_cnpj(cnpj):
    unique_chars = set(cnpj)
    if len(unique_chars) == 1:
        return False

    base_for_first_digit = cnpj[:12]
    expected_first_digit = calculate_first_digit(base_for_first_digit)
    
    base_second_digit = base_for_first_digit + expected_first_digit
    expected_second_digit = calculate_second_digit(base_second_digit)
    
    expected_cnpj = base_for_first_digit + expected_first_digit + expected_second_digit
    return expected_cnpj == cnpj

def validate_razao_social(razao_social):
    return not pd.isna(razao_social)

def validate_valor_despesas(valor_despesas):
    return valor_despesas > 0

df = pd.read_csv('./data/processed/consolidado_enriquecido.csv', dtype={'CNPJ': str})

df['CNPJ'] = df['CNPJ'].str.replace(r'\D', '', regex=True).str.zfill(14)

df_clean = df.dropna(subset=['CNPJ'])

df_clean['CNPJ_Valido'] = df_clean['CNPJ'].apply(validate_cnpj)
df_clean['Nome_Valido'] = df_clean['Razao_Social'].apply(validate_razao_social)
df_clean['Valor_Valido'] = df_clean['ValorDespesas'].apply(validate_valor_despesas)

print(df_clean.head())

output_file = "./data/processed/resultado_validado.csv"
df_clean.to_csv(output_file, index=False, encoding='latin1')




