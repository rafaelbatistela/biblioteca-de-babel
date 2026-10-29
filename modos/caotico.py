
import random

from gramatica.pontuacao import capitalizar


def gerar_texto_caotico(vocabulario, quantidade, semente=None):
    gerador = random.Random(semente)

    palavras_disponiveis = [
        palavra
        for categoria in vocabulario.values()
        if isinstance(categoria, list)
        for palavra in categoria
        if isinstance(palavra, str) and palavra.strip()
    ]

    if not palavras_disponiveis:
        raise ValueError("O vocabulário está vazio.")

    palavras = [
        gerador.choice(palavras_disponiveis)
        for _ in range(quantidade)
    ]

    texto = " ".join(palavras)

    return capitalizar(texto) + "."
