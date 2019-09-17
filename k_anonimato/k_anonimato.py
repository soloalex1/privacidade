import numpy as np
import pandas as pd

k = 2
df = pd.read_csv('k_anonimato/salario.csv')

# removendo atributos sensíveis
df.drop(columns=["id", "salario"], axis="columns", inplace=True)


def gen_localizacao(dataset):
    # adicionando coluna localização
    dataset.insert(0, 'localizacao', '*')

    freq_pais = dataset["pais"].value_counts()
    freq_estado = dataset["estado"].value_counts()
    freq_cidade = dataset["cidade"].value_counts()

    # generalizando localização
    for i in dataset.index:
        c = dataset.at[i, 'cidade']
        e = dataset.at[i, 'estado']
        p = dataset.at[i, 'pais']
        if freq_cidade.loc[c] < k:
            dataset.at[i, 'cidade'] = '*'
            if freq_estado.loc[e] < k:
                dataset.at[i, 'estado'] = '*'
                if freq_pais.loc[p] < k:
                    dataset.at[i, 'localizacao'] = '*'
                else:
                    dataset.at[i, 'localizacao'] = p
            else:
                dataset.at[i, 'localizacao'] = e + ', ' + p
        else:
            dataset.at[i, 'localizacao'] = c + ', ' + e + ', ' + p

    # removendo colunas extras: cidade, estado e país
    dataset.drop(columns=["cidade", "estado", "pais"], axis="columns", inplace=True)
    return dataset


def gen_data(dataset):
    freq_data = dataset["data"].value_counts()

    # verificando classes de equivalência para data: suprimindo dia
    for i in dataset.index:
        d = dataset.at[i, 'data']
        aux = d.split('/')
        if freq_data.loc[d] < k:
            aux[0] = '**'
        new_aux = aux[0] + '/' + aux[1] + '/' + aux[2]
        dataset.at[i, 'data'] = new_aux
    freq_data = dataset["data"].value_counts()

    # verificando classes de equivalência para data: suprimindo mês
    for i in dataset.index:
        d = dataset.at[i, 'data']
        aux = d.split('/')
        if freq_data.loc[d] < k:
            aux[1] = '**'
        new_aux = aux[0] + '/' + aux[1] + '/' + aux[2]
        dataset.at[i, 'data'] = new_aux
    freq_data = dataset["data"].value_counts()

    # verificando classes de equivalência para data: suprimindo ano
    for i in dataset.index:
        d = dataset.at[i, 'data']
        aux = d.split('/')
        if freq_data.loc[d] < k:
            aux[2] = '****'
        new_aux = aux[0] + '/' + aux[1] + '/' + aux[2]
        dataset.at[i, 'data'] = new_aux

    return dataset


def arvore_data(dataset):
    nivel0 = dataset.data.unique().tolist()

    lista_data = []
    nivel1 = dataset["data"].str.split("/", n=2, expand=True)

    mes = nivel1.iloc[:, 1]
    ano = nivel1.iloc[:, 2]

    for i in range(nivel1.shape[0]):
        lista_data.append(["**/" + mes[i] + "/" + ano[i]])

    nivel1 = pd.DataFrame(lista_data)
    nivel1 = nivel1[0].unique().tolist()

    nivel2 = []

    for i in range(0, ano.shape[0]):
        nivel2.append("**/**/" + ano[i])

    nivel2 = pd.DataFrame(nivel2)
    nivel2 = nivel2[0].unique().tolist()

    nivel3 = "**/**/****"

    arv = [nivel0, nivel1, nivel2, nivel3]

    return arv


df = gen_localizacao(df)
df = gen_data(df)

export_csv = df.to_csv(r'salario_2.csv', index=None, header=True)