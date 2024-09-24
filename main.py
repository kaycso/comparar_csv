import pandas as pd
import os
import glob
import logging

CSV_COLUMNS = ['camera', 'servidor']
CONSULTA_DIR = 'csv'
RESULTADO_DIR = 'resultado'

files_csv = glob.glob(os.path.join(CONSULTA_DIR, '*.csv'))

# Obter o arquivo Excel
df_excel = pd.read_excel('planilha.xlsx', sheet_name='folha1')[CSV_COLUMNS]

# Gerar um único DataFrame com os dados de todos os arquivos CSV
data_frames = []

for file in files_csv:
    df_csv = pd.read_csv(file)[CSV_COLUMNS] # obtendo o dataframe com as colunas desejadas
    data_frames.append(df_csv)

df_all_csv_files = pd.concat(data_frames, ignore_index=True).drop_duplicates()

# Realizando comparação com dos dados dos arquivos CSV com os dados do Excel
df_all_data = pd.merge(df_all_csv_files, df_excel, on=['camera', 'servidor'], how='outer', indicator=True)

# Obter os dados presentes no CSV que não estão no Excel
df_on_csv_exclusive = df_all_data[df_all_data['_merge'] == 'left_only'].drop('_merge', axis=1) 
df_on_csv_exclusive.to_csv(os.path.join(RESULTADO_DIR, 'resultado_csv_exclusivo.csv'), index=False) # salvando em um arquivo CSV

# Obter os dados presentes no Excel que não estão no CSV
df_on_excel_exclusive = df_all_data[df_all_data['_merge'] == 'right_only'].drop('_merge', axis=1) 

# Salvar os dados

df_on_excel_exclusive.to_csv(os.path.join(RESULTADO_DIR, 'resultado_excel_exclusivo.csv'), index=False)