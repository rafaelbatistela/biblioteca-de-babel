
def artigo_definido(palavra, genero="masculino", plural=False):
    """
    Retorna o artigo definido de acordo com gênero e número.
    """

    if genero == "feminino":
        return "as" if plural else "a"

    return "os" if plural else "o"


def artigo_indefinido(palavra, genero="masculino", plural=False):
    """
    Retorna o artigo indefinido de acordo com gênero e número.
    """

    if genero == "feminino":
        return "umas" if plural else "uma"

    return "uns" if plural else "um"


def combinar_artigo(palavra, genero="masculino", plural=False):
    """
    Combina artigo e palavra em uma expressão.
    """

    artigo = artigo_definido(
        palavra,
        genero=genero,
        plural=plural
    )

    return f"{artigo} {palavra}"
