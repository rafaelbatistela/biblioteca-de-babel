
def capitalizar(texto):
    """Coloca a primeira letra do texto em maiúscula."""

    texto = texto.strip()

    if not texto:
        return ""

    return texto[0].upper() + texto[1:]


def finalizar_frase(frase):
    """Garante pontuação final sem duplicar sinais."""

    frase = frase.strip()

    if not frase:
        return ""

    frase = frase.rstrip(".,;:!?")

    return frase + "."


def finalizar_texto(texto):
    """Capitaliza o texto e garante pontuação final."""

    texto = texto.strip()

    if not texto:
        return ""

    texto = texto.rstrip(" \n\t")

    if texto.endswith((".", "!", "?")):
        return capitalizar(texto)

    return finalizar_frase(capitalizar(texto))
