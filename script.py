import pandas as pd
import logging
import glob
from pathlib import Path
from datetime import datetime

# Configuração do logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Variáveis configuráveis
EXCEL_FILE = ' .xlsx'
EXCEL_SHEET = 'Folha1'
EXCEL_COLUMN = 'coluna1'
CSV_COLUMN = 'coluna1'  # Nome da coluna nos arquivos CSV
CONSULTA_DIR = Path('consulta')
OUTPUT_DIR = Path('comparativos')

# Função para ler o arquivo Excel
def read_excel_file(file, sheet):
    try:
        logger.info('Lendo o arquivo Excel...')
        return pd.read_excel(file, sheet_name=sheet)
    except FileNotFoundError:
        logger.error(f'O arquivo Excel {file} não foi encontrado.\n')
        raise
    except Exception as e:
        logger.error(f'Erro ao ler o arquivo Excel: {e}\n')
        raise

# Função para encontrar a coluna do CSV a ser comparada
def find_csv_column(df_csv):
    for col in df_csv.columns:
        if CSV_COLUMN.lower() in col.lower():
            return col
    return None

# Função para comparar os dados entre o CSV e o Excel
def compare_data(df_csv, df_excel, csv_column, excel_column):
    logger.info(f'Unindo os dados das colunas {csv_column} (CSV) e {excel_column} (Excel)...')
    merged_df = pd.merge(df_csv, df_excel, left_on=csv_column, right_on=excel_column, how='outer', indicator=True)
    result = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
    return result

# Função para processar os arquivos CSV
def process_csv_files(csv_files, df_excel, excel_column):
    all_results = pd.DataFrame()

    for csv_file in csv_files:
        logger.info(f'Lendo o arquivo CSV: {csv_file}')
        df_csv = pd.read_csv(csv_file)

        csv_column = find_csv_column(df_csv)
        if csv_column is None:
            logger.warning(f'Nenhuma coluna correspondente encontrada no CSV: {csv_file}')
            continue

        result = compare_data(df_csv, df_excel, csv_column, excel_column)
        all_results = pd.concat([all_results, result], ignore_index=True)

    return all_results.drop_duplicates()

# Função para salvar o resultado final
def save_results(all_results, result_file):
    logger.info(f'Salvando o resultado em {result_file}...')
    all_results.to_csv(result_file, index=False)
    logger.info('Resultado salvo com sucesso.\n')

# Função para gerenciar caminhos de pastas e arquivos
def get_file_paths():
    current_date = datetime.now().strftime('%m%d%Y')
    today_consulta_dir = CONSULTA_DIR / current_date
    result_file = OUTPUT_DIR / f'resultado_{datetime.now().strftime("%m_%d_%Y")}.csv'
    return today_consulta_dir, result_file

# Verificar se o arquivo Excel existe
if not Path(EXCEL_FILE).exists():
    logger.error(f'O arquivo Excel {EXCEL_FILE} não foi encontrado.\n')
    raise FileNotFoundError(f'Arquivo Excel {EXCEL_FILE} não encontrado.')

# Criar as pastas de consulta e comparativos, se não existirem
CONSULTA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Obter os caminhos da pasta de consulta do dia e do arquivo de resultado
today_consulta_dir, result_file = get_file_paths()

# Verificar se a pasta do dia existe e se há arquivos CSV
if not today_consulta_dir.exists():
    logger.error(f'A pasta {today_consulta_dir} não existe.\n')
    raise FileNotFoundError(f'A pasta {today_consulta_dir} não foi encontrada.')
else:
    csv_files = glob.glob(f'{today_consulta_dir}/*.csv')
    if not csv_files:
        logger.error(f'Nenhum arquivo CSV encontrado na pasta {today_consulta_dir}\n')
        raise FileNotFoundError(f'Nenhum arquivo CSV encontrado na pasta {today_consulta_dir}')

# Processo principal
try:
    # Ler o arquivo Excel
    df_excel = read_excel_file(EXCEL_FILE, EXCEL_SHEET)

    # Processar os arquivos CSV e comparar com o Excel
    all_results = process_csv_files(csv_files, df_excel, EXCEL_COLUMN)

    # Salvar o resultado
    save_results(all_results, result_file)

except Exception as e:
    logger.error(f'Ocorreu um erro durante o processo: {e}\n')