
import argparse
import json
from pathlib import Path

from modos.caotico import gerar_texto_caotico
from modos.poetico import gerar_texto_poetico
from modos.cientifico import gerar_texto_cientifico


def carregar_vocabulario():
    caminho = Path(__file__).parent / "dados" / "vocabulario.json"

    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def main():
    parser = argparse.ArgumentParser(
        description="Biblioteca de Babel — gerador experimental de textos"
    )

    parser.add_argument(
        "--modo",
        choices=["caotico", "poetico", "cientifico"],
        default="caotico",
        help="Modo de geração do texto"
    )

    parser.add_argument(
        "--palavras",
        type=int,
        default=30,
        help="Quantidade de palavras desejada"
    )

    parser.add_argument(
        "--semente",
        type=int,
        default=None,
        help="Semente para reproduzir a geração"
    )

    argumentos = parser.parse_args()

    if argumentos.palavras < 1:
        parser.error("A quantidade de palavras deve ser maior que zero.")

    try:
        vocabulario = carregar_vocabulario()

        geradores = {
            "caotico": gerar_texto_caotico,
            "poetico": gerar_texto_poetico,
            "cientifico": gerar_texto_cientifico
        }

        gerador = geradores[argumentos.modo]

        texto = gerador(
            vocabulario,
            argumentos.palavras,
            argumentos.semente
        )

    except (FileNotFoundError, json.JSONDecodeError) as erro:
        parser.error(f"Não foi possível carregar o vocabulário: {erro}")

    print("\n========== BIBLIOTECA DE BABEL ==========\n")
    print(texto)
    print("\n=========================================")
    print(f"Modo: {argumentos.modo}")
    print(f"Palavras solicitadas: {argumentos.palavras}")
    print(f"Palavras geradas: {len(texto.split())}")
    print(f"Semente: {argumentos.semente}")


if __name__ == "__main__":
    main()
