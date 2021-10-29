import os
from numpy.lib.function_base import append
import pandas as pd
from src.python.trata_receita import *

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'dados')
TRATADOS_DIR = os.path.join(DATA_DIR, 'dados_tratados')
DESPESA_DIR = os.path.join(DATA_DIR, 'Despesas')

M = 9
recurso = 0

def arquivos_despesa(M, DESPESA_DIR):
    arr_csv = [x for x in os.listdir(os.path.join(DESPESA_DIR, str(M))) if x.endswith(".csv")]
    return arr_csv

def tabela_despesa(M,recurso):
    
    df = pd.read_csv(os.path.join(DESPESA_DIR,str(M),arr_csv[recurso]), 
                    encoding='latin-1', 
                    #header=None,
                    skiprows= 4,
                    sep = ';',
                    decimal=',',
                    header=None
                    )
    df.columns = ['elemento', 'descricao', 'orçado', 'suplementado', 'empenhado', 'liquidado', 'pago', 'liq a pagar', 'saldo orç', 'lixo']

    del df['lixo']

    df['dot.atu'] = df[['descricao']].iloc[1:].append({'descricao': 0},ignore_index=True)
    df['reduzido'] = df[['elemento']].iloc[1:].append({'elemento': 0},ignore_index=True)

    contas = [
            '30000000000000000000',
            '33000000000000000000',

            '33100000000000000000',
            '33190040000000000000',
            '33190110000000000000',
            '33190113300000000000',
            '33190115200000000000',
            '33190130000000000000',
            '33190160000000000000',
            '33190460000000000000',
            '33190910000000000000',
            '33190940000000000000',
            '33191130000000000000',
            '33191130300000000000',
            '33191139900000000000',

            '33200000000000000000',

            '33300000000000000000',
            '33350000000000000000',
            '33390080000000000000',
            '33390300000000000000',
            '33390300100000000000',
            '33390300700000000000',
            '33390301600000000000',
            '33390302200000000000',
            '33390302600000000000',
            '33390302800000000000',
            '33390303500000000000',
            '33390303600000000000',
            '33390303900000000000',
            '33390305400000000000',
            '33390320000000000000',
            '33390320301000000000',
            '33390320310000000000',
            '33390330000000000000',
            '33390361500000000000',
            '33390370000000000000',
            '33390390000000000000',
            '33390391000000000000',
            '33390391200000000000',
            '33390391600000000000',
            '33390391900000000000',
            '33390392100000000000',
            '33390394300000000000',
            '33390394400000000000',
            '33390395000000000000',
            '33390395800000000000',
            '33390396700000000000',
            '33390397300000000000',
            '33390397800000000000',
            '33390398100000000000',
            '33390399901000000000',
            '33390399999000000000', #outros dos outros dos outros serviços de terceiros locação de mão de obra
            '33390400000000000000',
            '33390400400000000000',
            '33390400600000000000',
            '33390401300000000000',
            '33390401400000000000',
            '33390460000000000000',
            '33390471200000000000',
            '33390480000000000000',
            '33390490000000000000',
            '33390910000000000000',
            '33390920000000000000',
            '33390930000000000000',    
            
            '34000000000000000000',
            '34400000000000000000',
            '34450000000000000000',
            '34490510000000000000',
            '34490520000000000000',
            '34600000000000000000',

            '39999000000000000000'
        ]

    df2 = df[df['elemento'].isin(contas)]

    for coluna in ['orçado', 'suplementado', 'empenhado', 'liquidado', 'pago', 'liq a pagar', 'saldo orç', 'dot.atu', 'reduzido']:
        df2[coluna] = transforma_numero(df2[coluna])

    df2 = df2[['elemento', 'descricao','orçado', 'suplementado', 'reduzido', 'dot.atu', 'empenhado', 'liquidado', 'pago', 'liq a pagar', 'saldo orç']]

    df2['mes'] = M
    df2['vinculo'] = vinculo[recurso]

    return df2


def trata_despesa(inicial, final):
    first = True
    for M in range(inicial, final + 1):
        arr_csv = arquivos_despesa(M, DESPESA_DIR)
        vinculo = [x.replace('.csv','') for x in arr_csv]
        for recurso in range(0,len(arquivos_despesa(M, DESPESA_DIR))):
            if first:
                try:
                    df = tabela_despesa(M, recurso)
                except:
                    None
            else:
                try:
                    df = append(tabela_despesa(M, recurso))
                except:
                    None

    df.to_csv(os.path.join(TRATADOS_DIR, 'despesas power bi.csv'), index=None, sep = ';', decimal = ',')

    df = pd.pivot_table(df, 
                        values = 'pago', 
                        columns = 'mes', 
                        index=['Vinculo','elemento', 'descricao'], 
                        aggfunc = 'sum'
                        )

    df.to_csv(os.path.join(TRATADOS_DIR, 'despesas mes a mes.csv'), sep = ';', decimal = ',')