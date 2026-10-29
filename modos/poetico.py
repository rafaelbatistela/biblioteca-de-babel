
import random

from gramatica.estruturas import gerar_estrutura
from gramatica.pontuacao import finalizar_texto


MOLDES_POETICOS = [
    "{natureza} {verbo} {adverbio}.",
    "{sentimento} {verbo} no silêncio.",
    "O tempo {verbo} entre as estrelas.",
    "A memória {verbo} como a névoa.",
    "Entre o silêncio e a tempestade, {natureza} {verbo}.",
    "Talvez a saudade {verbo} sob a lua.",
    "A noite guarda {sentimento} no infinito.",
    "{natureza} dança onde a memória adormece.",
]


def adicionar_artigo(palavra):
    """Evita adicionar outro artigo quando a palavra já possui um."""

    palavra = palavra.strip()

    if palavra.lower().startswith(("a ", "o ", "as ", "os ")):
        return palavra

    return f"a {palavra}"


def gerar_texto_poetico(vocabulario, quantidade, semente=None):
    gerador = random.Random(semente)

    naturezas = vocabulario.get(
        "elementos_natureza",
        ["lua", "mar", "vento", "floresta"]
    )

    sentimentos = vocabulario.get(
        "sentimentos",
        ["saudade", "medo", "esperança", "solidão"]
    )

    verbos = vocabulario.get(
        "verbos_poeticos",
        ["sussurra", "floresce", "desaparece", "renasce"]
    )

    adverbios = vocabulario.get(
        "adverbios",
        ["lentamente", "eternamente", "misteriosamente"]
    )

    if not all([naturezas, sentimentos, verbos, adverbios]):
        raise ValueError("Uma categoria do vocabulário poético está vazia.")

    naturezas = [adicionar_artigo(p) for p in naturezas]
    sentimentos = [adicionar_artigo(p) for p in sentimentos]

    frases = []
    total = 0

    while total < quantidade:
        valores = {
            "natureza": gerador.choice(naturezas),
            "sentimento": gerador.choice(sentimentos),
            "verbo": gerador.choice(verbos),
            "adverbio": gerador.choice(adverbios),
        }

        # Gera a frase usando a ferramenta de estruturas.
        frase = gerar_estrutura(
            MOLDES_POETICOS,
            valores,
            gerador
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
