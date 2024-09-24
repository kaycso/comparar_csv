import pandas as pd

my_data_set= {
    'cars': ["BMW", "Volvo", "Ford"],
    'passings': [3, 7, 2]
}

print(my_data_set, type(my_data_set))

my_var = pd.DataFrame(my_data_set)

print(my_var)
print(type(my_var))

a = [1, 7, 2]
my_var_series = pd.Series(a)
print(my_var_series)
print(type(my_var_series))
print(my_var_series[0])

my_var_series_labels = pd.Series(a, index=["x","y","z"])
print(my_var_series_labels)
print(my_var_series_labels["x"])

calories = { "day1": 420, "day2": 380, "day3": 390 }

series_calories = pd.Series(calories)

print(series_calories)
print(series_calories["day1"])

series_calories_2 = pd.Series(calories, index=["day1", "day2"])
print(series_calories_2)

data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45]
}

df = pd.DataFrame(data)
print(df)
print(df.loc[0])
print(df.loc[[0, 1]])

df = pd.DataFrame(data, index = ["day1", "day2", "day3"])
print(df.loc["day1"])
print(df.loc[["day1", "day2"]])

data_frame = pd.read_csv('data.csv')
print(data_frame)

print(pd.options.display.max_rows)

data = {
  "Duration":{
    "0":60,
    "1":60,
    "2":60,
    "3":45,
    "4":45,
    "5":60
  },
  "Pulse":{
    "0":110,
    "1":117,
    "2":103,
    "3":109,
    "4":117,
    "5":102
  },
  "Maxpulse":{
    "0":130,
    "1":145,
    "2":135,
    "3":175,
    "4":148,
    "5":127
  },
  "Calories":{
    "0":409,
    "1":479,
    "2":340,
    "3":282,
    "4":406,
    "5":300
  }
}

df = pd.DataFrame(data)

print(df) 

df = pd.read_csv('data.csv')

print(df.head(10))
print(df.info(), '\n')


calories = df["Calories"]
print(calories)

# obter o arquivo CSV
# obter o arquivo Excel
# comparar se a câmera e servidor do csv é a mesma (camera e servidor) do excel
#   Caso não, é necessário criar um arquivo csv com o resultado das câmeras que estão no CSV mas não estão no Excel
#   Caso sim, é necessário criar um arquivo II
df_csv = pd.read_csv('arquivo.csv')
df_excel = pd.read_excel('planilha.xlsx', sheet_name='folha1')
df_csv_filtrado = df_csv[['camera', 'servidor']]
df_excel_filtrado = df_excel[['camera', 'servidor']]

df_comparacao = pd.merge(df_csv_filtrado, df_excel_filtrado, on=['camera', 'servidor'], how='outer', indicator=True)
df_resultado_csv = df_comparacao[df_comparacao['_merge'] == 'left_only'].drop('_merge', axis=1)
df_resultado_excel = df_comparacao[df_comparacao['_merge'] == 'right_only'].drop('_merge', axis=1)

df_resultado_csv.to_csv('resultado_csv.csv', index=False)
df_resultado_excel.to_csv('resultado_excel.csv', index=False)

print(df_comparacao)

# Necessário fazer a verificação de todos os arquivos em uma pasta especificada
