import os 

os.system('cls')


import pandas as pd


import numpy as np

# df_cadastro = pd.read_csv('tb_CadastroProdutos2017_Miranda.csv')
# print(df_cadastro)

# df_vendas = pd.read_csv('tb_Vendas2017_Miranda.csv')
# print(df_vendas)


try:
    print('Obtendo dados...')
    

    df_vendas = pd.read_csv(
        'tb_Vendas2017_Miranda.csv', sep=';', encoding='iso-8859-1')
    df_cadastro = pd.read_csv(
        'tb_CadastroProdutos2017_Miranda.csv', sep=';', encoding='iso-8859-1')
    
    df_qvendas = df_vendas[['ID Produto', 'Quantidade Vendida']]
    df_produtos = df_cadastro[['ID Produto', 'Preco Unitario']]
    print(df_produtos)
    print(df_qvendas)


    # df_produtos = df_cadastro[['Quantidade Vendida']]

    # df_vendido = df_vendido.groupby(
    #     ['Id Produto']).sum(['Quantidade Vendida']).reset_index()

    # print(df_vendido.head())
    print('Dados obtidos com sucesso!')


except Exception as e:
    print(f'Erro ao obter dados {e}')
    exit()


try:
    array_quantidade_vendida = np.array(df_qvendas['Quantidade Vendida'])

    media = np.mean(array_quantidade_vendida)
    mediana = np.median(array_quantidade_vendida)
    distancia_media_mediana = ((media-mediana)/mediana *100)
   

    q1 = np.quantile(array_quantidade_vendida, 0.25, method='weibull')
    q3 = np.quantile(array_quantidade_vendida, 0.75, method='weibull')
    iqr = q3 - q1
    minimo = np.min(array_quantidade_vendida)
    limite_inferior = q1 - (1.5*iqr)
    limite_superior = q3 + (1.5*iqr)
    maximo = np.max(array_quantidade_vendida)
    amplitute_total = maximo - minimo

    print(f'Média: {media}')
    print(f'Mediana: {mediana}')
    print(f'Distância Media e Mediana: {distancia_media_mediana}')
    print(f'Q1: {q1}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Minimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')
    print(f'Amplitude Total: {amplitute_total}')


    df_recup_quantidade_vendida_sup = df_qvendas[
        df_qvendas['Quantidade Vendida'] > limite_superior]
    
    print('\nQuantidade Vendida superiores as demais:')
    print(30*'-')
    if len(df_recup_quantidade_vendida_sup) == 0:
        print('Não existem DPs com valores discrepantes superiores')
    else:
        print(df_recup_quantidade_vendida_sup.sort_values(
            by='recuperacao_veiculos', ascending=False))
    
    
    df_recup_veiculo_outliers_inf = df_recup_veiculo[
        df_recup_veiculo['recuperacao_veiculos'] > limite_inferior]
    
    print('\nDPs com recuperações inferiores as demais:')
    print(30*'-')
    if len(df_recup_veiculo_outliers_inf) == 0:
        print('Não existem DPs com valores discrepantes inferiores')
    else:
        print(df_recup_veiculo_outliers_inf.sort_values(
            by='recuperacao_veiculos', ascending=False).to_string())

except Exception as e:
    print(f'Erro ao obter dados {e}')
    exit()
