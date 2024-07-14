import os
import glob
import pandas as pd
import numpy as np

print("Lendo os Arquivos")
df1 = pd.read_csv(r"C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\MUNICIPIOS_LAT_LONG.csv", delimiter=';')
df2 = pd.read_csv(r"C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\lista_enderecos.del", delimiter='|', encoding='latin1')

# Convert 'MATRICULA' column to integer in df2
df2['Mat_calc'] = df2['Mat_calc'].astype(int)

print("Fazendo o join")
# Convertendo as colunas relevantes para minúsculas
df1['Municipio'] = df1['Municipio'].str.lower()
df1['Logradouro'] = df1['Logradouro'].str.lower()
df2['Nome_Localidade'] = df2['Nome_Localidade'].str.lower()
df2['Nome_logradouro'] = df2['Nome_logradouro'].str.lower()

# Fazendo o outer join
df = pd.merge(df1, df2, how='outer', left_on=['Municipio', 'Logradouro'], right_on=['Nome_Localidade', 'Nome_logradouro'])

# Selecionando as colunas desejadas
df = df[['Unidade', 'Gerencia', 'Nome_Localidade', 'Nome_bairro', 'Tp_log', 'Nome_logradouro', 'Mat_calc', 'LAT', 'LONG']]

# Define the directory where the txt files are located
directory = r"C:\Files\Leitura\Dados\5RM3\Fases"

# Define the keywords to search in the file names
keywords = ["unce", "unle", "unmt", "unnt", "unoe", "unsl"]

# Get the list of all txt files in the directory
files = glob.glob(os.path.join(directory, "*.txt"))

# Filter the files based on the keywords and get the latest modified file for each keyword
latest_files = []
for keyword in keywords:
    keyword_files = [file for file in files if keyword in file]
    latest_file = max(keyword_files, key=os.path.getmtime)
    latest_files.append(latest_file)

# Initialize an empty dataframe to store the final results
df_txt_final = pd.DataFrame()

print("Consultando as Fases")
# Read the latest files, join with the csv data, and append the results to df_final
for file in latest_files:
    print(f"Lendo Fase {file}")
    df_txt = pd.read_csv(file, delimiter=';', encoding='latin1', usecols=['MATRICULA', 'OCORRENCIA'])
    df_txt['MATRICULA'] = df_txt['MATRICULA'].astype(int)
    df_txt_final = pd.concat([df_txt_final, df_txt])

# Now we can join df and df_txt_final
df_final = pd.merge(df, df_txt_final, how='left', left_on='Mat_calc', right_on='MATRICULA')

df_final = df_final[['Unidade', 'Gerencia', 'Nome_Localidade', 'Nome_bairro', 'Tp_log', 'Nome_logradouro', 'Mat_calc', 'OCORRENCIA', 'LAT', 'LONG']]

print("Gerando os arquivos!")
# Save the final results to a csv file and a parquet file
df_final.to_csv(r"C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\mapa.csv", index=False)
df_final.to_parquet(r"C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\mapa.parquet")

print("Concluído")
