import os 

os.system('cls')


import pandas as pd


import numpy as np



df = pd.read_excel('vendas_eletos_eletronicos2.xlsx')
print(df)

total_vendas = df['Vendas (unidades)']
valor_total = df['Total']


mediana = np.median(valor_total)
print(f'\nMediana do total vendido {mediana}')

media = np.mean(valor_total)
print(f'Média do total vendido {media}\n')

q1 = np.quantile(total_vendas, 0.25)
q2 = np.quantile(total_vendas, 0.50)
q3 = np.quantile(total_vendas, 0.75)

print(f'25% dos produtos vendidos estão abaixo de: {q1} unidades vendias')
print(f'50% dos produtos vendidos estão abaixo de: {q2} unidades vendidas')
print(f'75% dos produtos vendidos estão abaixo de: {q3} unidades vendidas\n')


totalvdd_organizada = df.sort_values(by='Vendas (unidades)', ascending=True)
total_vendas = totalvdd_organizada['Vendas (unidades)']


print('Filtragem de Vendas: ')
filtro_vendas = q3
mais_vendidos = df[df['Vendas (unidades)'] > filtro_vendas] 
print(mais_vendidos[['Nome do Produto', 'Vendas (unidades)']])
print(150* '=')

