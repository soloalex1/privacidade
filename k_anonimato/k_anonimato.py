import numpy as np
import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder

# lendo dataset
df = pd.read_csv("k_anonimato/salario.csv")

# agrupando os atributos de localidade
entry_ids = df.id
entry_cidades = df.cidade
entry_estados = df.estado
entry_paises = df.pais

local_full = []
for i in range(len(entry_cidades)):
    local_full.append([entry_ids[i], str("{}, {}, {}".format(entry_cidades[i], entry_estados[i], entry_paises[i]))])

df_local = pd.DataFrame(local_full, columns=["id", "localidade"])
df = pd.concat([df, df_local], axis="columns", join="inner")

# removendo os identificadores e atributos sensíveis
df.drop(columns=["id", "pais", "cidade", "estado"], inplace=True)
df.dropna(inplace=True)

# codificando gênero pra {0 = Female, 1 = Male}
gen_encoder = [(["genero"], LabelEncoder())]
mapper = DataFrameMapper(gen_encoder, df_out=True)
col_novas = mapper.fit_transform(df.copy())

# removendo a coluna original e adicionando a codificada
df = pd.concat([df.drop(columns=["genero"]), col_novas], axis="columns")

df.shape
df.head()

# salvando o dataset modificado
export_csv = df.to_csv(r'salario_2.csv', index=None, header=True)