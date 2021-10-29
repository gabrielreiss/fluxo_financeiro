import os
import pandas as pd

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'dados')
TRATADOS_DIR = os.path.join(DATA_DIR, 'dados_tratados')
RECEITA_DIR = os.path.join(DATA_DIR, 'Receitas')

pd.options.display.float_format = '{:.2f}'.format

def transforma_numero(df):
    df = df.str.replace('(','-')
    df = df.str.replace(')','')
    df = df.str.replace('.','')
    df = df.str.replace(',','.')
    df = pd.to_numeric(df)
    return df

def arquivos(M):
    arr_csv = [x for x in os.listdir(os.path.join(RECEITA_DIR, str(M))) if x.endswith(".csv")]
    return arr_csv

def trata_receita(M,recurso):
    arr_csv = arquivos(M)
    vinculo = [x.replace('.csv','') for x in arr_csv]

    df = pd.read_csv(os.path.join(RECEITA_DIR,str(M),arr_csv[recurso]), 
                    encoding='latin-1', 
                    #header=None,
                    skiprows= 0,
                    sep = ';',
                    decimal=','
                    )

    df['Orçado Atualizado'] = transforma_numero(df['Orçado Atualizado'])
    df['Arrecadado'] = transforma_numero(df['Arrecadado'])
    df['Vinculo'] = vinculo[recurso]
    df['Mes'] = M

    df = df[['Descrição', 'Conta Receita', 'Vinculo', 'Orçado Atualizado', 'Arrecadado', 'Mes']]

    #Seleciona contas para base de calculo
    contas = [
        '40000000000000000000',
        '41000000000000000000',
        '41100000000000000000',
        '41200000000000000000',
        '41300000000000000000',
        '41600000000000000000',
        '41700000000000000000',
        '41900000000000000000',
        '42000000000000000000',
        '42100000000000000000',
        '42200000000000000000',
        '42400000000000000000',
        '90000000000000000000'
    ]

    df2 = df[df['Conta Receita'].isin(contas)]

    return df2

def exporta_receita(inicial, final):
    first = True
    
    for M in range(inicial,final +1):
        for recurso in range(0,len(arquivos(M))):
            if first:        
                try:
                    df = trata_receita(M, recurso)
                except:
                    None
                first = False
            else:
                try:
                    df = df.append(trata_receita(M,recurso))
                except:
                    None

    df.to_csv(os.path.join(TRATADOS_DIR, 'receitas power bi.csv'), index=None, sep = ';', decimal = ',')

    df = pd.pivot_table(df, 
                    values = 'Arrecadado', 
                    columns = 'Mes', 
                    index=['Vinculo','Conta Receita', 'Descrição'], 
                    aggfunc = 'sum'
                    )

    df.to_csv(os.path.join(TRATADOS_DIR, 'receitas mes a mes.csv'), sep = ';', decimal = ',')