import numpy as np
import pandas as pd

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


# suprimindo o atributo de genero
def suppression(data, field):
    for el in range(len(data)):
        data.iloc[el][field] = "*"
    return data


df = suppression(df, "genero")
df.shape
df.head()

# salvando o dataset modificado
export_csv = df.to_csv(r'salario_2.csv', index=None, header=True)