
import random


def gerar_estrutura(modelos, valores, gerador=None):
    """
    Escolhe um modelo de frase e preenche seus campos.

    Exemplo de modelo:
    "A {causa} influencia {efeito}."
    """

    if not modelos:
        raise ValueError("A lista de modelos está vazia.")

    if gerador is None:
        gerador = random.Random()

    modelo = gerador.choice(modelos)

    try:
        return modelo.format(**valores)
    except KeyError as erro:
        campo = erro.args[0]
        raise ValueError(
            f"Está faltando um valor para o campo '{campo}'."
        ) from erro
