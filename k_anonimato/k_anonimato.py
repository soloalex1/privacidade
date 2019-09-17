import numpy as np
import pandas as pd

k = 2
df = pd.read_csv('k_anonimato/salario.csv')

# removendo atributos sensíveis
df.drop(columns=["id", "salario"], axis="columns", inplace=True)


def precisao(dataset, semi, h, alt):
    soma = 0
    for i in range(semi):
        for j in range(dataset):
            soma += (h[j] / alt[i])

    return 1 - (soma / (dataset * semi))


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


def gen_genero(dataset):
    for i in range(len(dataset):
        dataset.iloc[i]['genero'] = "*" 
    return dataset



df = gen_localizacao(df)
df = gen_data(df)
df = gen_genero(df)       
                                                                     

export_csv = df.to_csv(r'salario_2.csv', index=None, header=True)
