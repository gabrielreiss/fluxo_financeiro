import os
import pandas as pd

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'dados')
TRATADOS_DIR = os.path.join(DATA_DIR, 'dados_tratados')


receita = pd.read_csv(
    os.path.join(DATA_DIR, 'Receitas', "Receita Orçada e Arrecadada Mês a Mês 2021-09.csv"),
    encoding='latin-1',
    header=None,
    skiprows= 2,
    sep = ';',
    decimal=','
)
receita = receita.iloc[:,0:15]
receita.columns = ['conta', 'orcado', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']


