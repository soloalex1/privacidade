import numpy as np
import pandas as pd

# lendo dataset
df = pd.read_csv('salario.csv')

# removendo o identificador explícito
df.drop(columns=["id"])

# codificando gênero pra {0, 1}
encoder = [(["genero"], LabelEncoder())]
mapper = DataFrameMapper(encoder, df_out=True)
col_novas = mapper.fit_transform(df.copy())

df.shape()
df.head()

export_csv = df.to_csv(r'salario_2.csv', index=None, header=True)
