import numpy as np
import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder

# lendo dataset
df = pd.read_csv("k_anonimato/salario.csv")

# removendo o identificador explícito
df.drop(columns=["id"], inplace=True)
df.dropna(inplace=True)

# codificando gênero pra {0, 1}
encoder = [(["genero"], LabelEncoder())]
mapper = DataFrameMapper(encoder, df_out=True)
col_novas = mapper.fit_transform(df.copy())
df = pd.concat([df.drop(columns=["genero"]), col_novas], axis="columns")

df.shape
print (df.head())

export_csv = df.to_csv(r'salario_2.csv', index=None, header=True)