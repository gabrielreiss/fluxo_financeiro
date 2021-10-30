from src.python.trata_receita import *
from src.python.trata_bancos import *
from src.python.trata_despesa import *

inicial = 9
final = 9

exporta_receita(inicial, final)
trata_banco()
trata_despesa(inicial, final)