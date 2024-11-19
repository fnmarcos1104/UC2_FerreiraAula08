import os 

os.system('cls')
import pandas as pd
import numpy as np


try:
    print('Obtendo dados...')

    # CSV VENDAS 2017 MIRANDA
    df_dados_vendas = pd.read_csv(
        'tb_Vendas2017_Miranda.csv', sep=';', encoding='iso-8859-1')
    
    # SELECIONANDO SOMENTE AS VARIÁVEIS
    df_vendas = df_dados_vendas[['Numero da Venda',
                                 'ID Produto', 'ID Cliente', 'Quantidade Vendida']]
    
    print()
    print(df_vendas.head())

    # CSV CADASTRO DE PRODUTOS 2017 MIRANDA
    df_dados_produtos = pd.read_csv(
        'tb_CadastroProdutos2017_Miranda.csv', sep=';', encoding='utf-8')
    
    print()
    print(df_dados_produtos.head())

    df_produtos = df_dados_produtos[[
        'Nome da Marca', 'Tipo', 'Preco Unitario', 'ID Produto'
    ]]

    df_produtos.loc[:, 'Preco Unitario'] = df_produtos[
        'Preco Unitario'].str.replace(',', '.').astype(float)
    
    print()
    print(df_produtos.head())
    print('Dados obtidos com sucesso')


except Exception as e:
    print(f'Erro ao obter dados {e}')
    exit()


try:
    print('Processando...')

    # Juntando os dataframes df_vendas e df_produtos usando a coluna 'ID Produto'
    df_produtos_vendidos = pd.merge(df_vendas, df_produtos, on='ID Produto')
    print()
    print(df_produtos_vendidos)

    df_produtos_vendidos['Valor Total'] = df_produtos_vendidos['Quantidade Vendida'] * df_produtos_vendidos['Preco Unitario']

    df_produtos_vendidos = df_produtos_vendidos.groupby('Nome da Marca').agg({
        'Quantidade Vendida': 'sum',
        'Valor Total': 'sum'
    }).reset_index()

except ImportError as e:
    print(f'Erro ao obter dados: {e}')
    exit()

try:
    array_produtos_vendidos = np.array(df_produtos_vendidos['Valor Total'])


    # Calcula a media
    media_produtos_vendidos = np.mean(array_produtos_vendidos)
    # Calcula Mediana
    mediana_produtos_vendidos = np.median(array_produtos_vendidos)
    # Distância
    distancia = abs(
        (media_produtos_vendidos - mediana_produtos_vendidos) / mediana_produtos_vendidos
    ) * 100

    print()
    print(f'Média: {media_produtos_vendidos}')
    print(f'Mediana: {mediana_produtos_vendidos}')
    print(f'Distância: {distancia}')

    maximo = np.max(array_produtos_vendidos)
    minimo = np.min(array_produtos_vendidos)
    amplitude = maximo - minimo

    print(f'\nMáximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude: {amplitude}')

    q1 = np.quantile(
        array_produtos_vendidos, 0.25, method='weibull') # 25%
    q2 = np.quantile(
        array_produtos_vendidos, 0.50, method='weibull') # 50%
    q3 = np.quantile(
        array_produtos_vendidos, 0.75, method='weibull') # 75%
    
    iqr = q3 - q1
    # Limite superior - Identifica os outliers acima de Q3  
    limite_superior = q3 + (1.5 * iqr)
    # Limite inferior - Identifica os outliers abaixo de Q1  
    limite_inferior = q1 - (1.5 * iqr)

    print(f'\nQ1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Limite Inferior: {limite_inferior}')

    # Filtrar o dataframe df_produtos_vendidos p/ obter outliers inferiores
    df_produtos_vendidos_outliers_inferiores = df_produtos_vendidos[df_produtos_vendidos['Valor Total'] < limite_inferior]
    # Filtrar o dataframe df_produtos_vendidos p/ obter outliers superiores
    df_produtos_vendidos_outliers_superiores = df_produtos_vendidos[df_produtos_vendidos['Valor Total'] > limite_superior]

    
    # Print Outliers INFERIORES
    print('\nOutliers Inferiores')
    print(30*'-')
    if len(df_produtos_vendidos_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
    else:
        print(df_produtos_vendidos_outliers_inferiores.sort_values(by='Valor Total', ascending=True))

    # Print Outliers SUPERIORES
    print('\nOutliers Superiores')
    print(30*'-')
    if len(df_produtos_vendidos_outliers_superiores) == 0:
        print('Não existem outliers Superiores!')
    else:
        print(df_produtos_vendidos_outliers_superiores.sort_values(by='Valor Total', ascending=False))

except ImportError as e:
    print(f'Erro ao obter dados: {e}')
    exit()