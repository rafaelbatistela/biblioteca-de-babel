
import json
import random
from pathlib import Path

from gramatica.estruturas import gerar_estrutura
from gramatica.pontuacao import finalizar_texto


MOLDES_CIENTIFICOS = [
    "O fenômeno observado envolve {fenomeno}.",
    "A análise considera {conceito} no contexto de {fenomeno}.",
    "Os resultados sugerem uma relação entre {conceito} e {fenomeno}.",
    "O estudo de {conceito} contribui para compreender {fenomeno}.",
    "Nesse contexto, {fenomeno} está associado a {conceito}.",
    "A investigação de {fenomeno} permite analisar {conceito}.",
]


def carregar_vocabulario_cientifico():
    caminho = (
        Path(__file__).parent.parent
        / "dados"
        / "vocabulario_cientifico.json"
    )

    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def selecionar_termo(lista, gerador):
    if not lista:
        raise ValueError("Uma categoria do vocabulário está vazia.")

    return gerador.choice(lista)


def gerar_texto_cientifico(vocabulario, quantidade, semente=None):
    gerador = random.Random(semente)

    # Carrega o vocabulário científico separado.
    vocabulario_cientifico = carregar_vocabulario_cientifico()

    # Escolhe uma área científica disponível.
    areas = [
        area
        for area, categorias in vocabulario_cientifico.items()
        if isinstance(categorias, dict)
        and categorias.get("conceitos")
        and categorias.get("fenomenos")
    ]

    if not areas:
        raise ValueError(
            "Não existem áreas científicas com conceitos e fenômenos."
        )

    frases = []
    total = 0

    while total < quantidade:
        area = gerador.choice(areas)
        categorias = vocabulario_cientifico[area]

        conceito = selecionar_termo(
            categorias["conceitos"], gerador
        )

        fenomeno = selecionar_termo(
            categorias["fenomenos"], gerador
        )

        valores = {
            "conceito": conceito,
            "fenomeno": fenomeno,
        }

        frase = gerar_estrutura(
            MOLDES_CIENTIFICOS,
            valores,
            gerador,
        )

        frase = finalizar_texto(frase)
        palavras = frase.split()
        faltam = quantidade - total

        # Mantém a quantidade solicitada.
        if len(palavras) > faltam:
            palavras = palavras[:faltam]

        if palavras:
            frase_final = " ".join(palavras).rstrip(".,;:!?") + "."
            frases.append(frase_final)
            total += len(palavras)

    return finalizar_texto(" ".join(frases))
