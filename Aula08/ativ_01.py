import os

os.system('cls')

import pandas as pd 


from sqlalchemy import create_engine


import numpy as np



#Obter dados
try:
    print('Obtendo dados...')
    ENDEREÇO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(
        ENDEREÇO_DADOS, sep=';', encoding='iso-8859-1')
    
    # DELIMITANDO SOMENTE AS VARIÁVEIS DE DELEGACIA
    df_recup_veiculo = df_ocorrencias[['cisp', 'recuperacao_veiculos']]

    df_recup_veiculo = df_recup_veiculo.groupby(
        ['cisp']).sum(['recuperecao_veiculos']).reset_index()

    print(df_recup_veiculo.head())
    print('Dados obtidos com sucesso!')


except Exception as e:
    print(f'Erro ao obter dados {e}')
    exit()



try:
    array_recup_veiculo = np.array(df_recup_veiculo['recuperacao_veiculos'])

    media = np.mean(array_recup_veiculo)
    mediana = np.median(array_recup_veiculo)
    distancia_media_mediana = ((media-mediana)/mediana *100)
   

    q1 = np.quantile(array_recup_veiculo, 0.25, method='weibull')
    q3 = np.quantile(array_recup_veiculo, 0.75, method='weibull')
    iqr = q3 - q1
    minimo = np.min(array_recup_veiculo)
    limite_inferior = q1 - (1.5*iqr)
    limite_superior = q3 + (1.5*iqr)
    maximo = np.max(array_recup_veiculo)
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

    df_recup_veiculo_outliers_sup = df_recup_veiculo[
        df_recup_veiculo['recuperacao_veiculos'] > limite_superior]
    
    print('\nDPs com recuperações superiores as demais:')
    print(30*'-')
    if len(df_recup_veiculo_outliers_sup) == 0:
        print('Não existem DPs com valores discrepantes superiores')
    else:
        print(df_recup_veiculo_outliers_sup.sort_values(
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


