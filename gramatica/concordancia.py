

def artigo_definido(genero="masculino", plural=False):
    artigos = {
        ("masculino", False): "o",
        ("feminino", False): "a",
        ("masculino", True): "os",
        ("feminino", True): "as",
    }

    return artigos[(genero, plural)]


def artigo_indefinido(genero="masculino", plural=False):
    artigos = {
        ("masculino", False): "um",
        ("feminino", False): "uma",
        ("masculino", True): "uns",
        ("feminino", True): "umas",
    }

    return artigos[(genero, plural)]


def combinar_artigo(
    palavra,
    genero="masculino",
    plural=False,
    definido=True
):
    artigo = (
        artigo_definido(genero, plural)
        if definido
        else artigo_indefinido(genero, plural)
    )

    return f"{artigo} {palavra}"
