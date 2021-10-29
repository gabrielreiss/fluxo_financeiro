import os
import pandas as pd
from src.python.trata_receita import *

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'dados')
TRATADOS_DIR = os.path.join(DATA_DIR, 'dados_tratados')
BANCOS_DIR = os.path.join(DATA_DIR, 'Bancos')

pd.options.display.float_format = '{:.2f}'.format

def trata_banco():
    arr_csv = [x for x in os.listdir(BANCOS_DIR) if x.endswith(".csv")]

    first =True
    for i in range(0,len(arr_csv)):

        M = int(arr_csv[i].split('-')[1].split('.')[0])

        try:
            df = pd.read_csv(os.path.join(BANCOS_DIR,arr_csv[i-1]), 
                                encoding='latin-1', 
                                #header=None,
                                skiprows= 2,
                                sep = ';',
                                decimal=','
                                )

            df.columns = ['cod', 'descricao', 'conta corrente', 'vinculo', 'descr vinculo', 'Saldo anterior', 'debitos', 'creditos', 'saldo atual', 'erro']

            for coluna in ['Saldo anterior', 'debitos', 'creditos', 'saldo atual']:
                df[coluna] = transforma_numero(df[coluna])

            df_filtrada = df[['vinculo', 'Saldo anterior', 'debitos', 'creditos', 'saldo atual']]

            bancos = df_filtrada.groupby(['vinculo'],as_index = False).sum()
            bancos['mes'] = M
            if first:
                banco_export = bancos
                first = False
            else:
                banco_export = banco_export.append(bancos)

            saldo_anterior = banco_export.pivot_table(values = "Saldo anterior",
                                columns = "mes",
                                index = "vinculo")

            saldo_atual =  banco_export.pivot_table(values = "saldo atual",
                                columns = "mes",
                                index = "vinculo")

            banco_export.to_csv(os.path.join(TRATADOS_DIR, 'bancos.csv'), index=None, sep = ';', decimal = ',')
            saldo_anterior.to_csv(os.path.join(TRATADOS_DIR, 'saldo_anterior.csv'), sep = ';', decimal = ',')
            saldo_atual.to_csv(os.path.join(TRATADOS_DIR, 'saldo_atual.csv'), sep = ';', decimal = ',')

        except:
            None
