
from gramatica.concordancia import combinar_artigo
from gramatica.estruturas import gerar_estrutura
from gramatica.pontuacao import finalizar_texto

import random


print(combinar_artigo("floresta", genero="feminino"))
print(combinar_artigo("universo", genero="masculino"))

modelo = [
    "A {causa} influencia {efeito}."
]

valores = {
    "causa": "temperatura",
    "efeito": "sistema"
}

frase = gerar_estrutura(
    modelo,
    valores,
    random.Random(42)
)

print(finalizar_texto(frase))
