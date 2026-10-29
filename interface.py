
import random
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from modos.caotico import gerar_texto_caotico
from modos.poetico import gerar_texto_poetico
from modos.cientifico import gerar_texto_cientifico
from main import carregar_vocabulario


# Configuração visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


FUNDO = "#111114"
PAINEL = "#1B1B20"
DOURADO = "#C8A978"
TEXTO = "#F1E7D5"
SECUNDARIO = "#A69A88"


class BibliotecaDeBabel(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Biblioteca de Babel")
        self.geometry("900x720")
        self.minsize(700, 620)
        self.configure(fg_color=FUNDO)

        self.vocabulario = carregar_vocabulario()
        self.modo_selecionado = tk.StringVar(value="poetico")
        self.semente = tk.StringVar(value="")
        self.quantidade = tk.IntVar(value=30)

        self.criar_interface()

    def criar_interface(self):
        # Cabeçalho
        cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        cabecalho.pack(fill="x", padx=35, pady=(30, 20))

        ctk.CTkLabel(
            cabecalho,
            text="BIBLIOTECA DE BABEL",
            font=("Georgia", 28, "bold"),
            text_color=DOURADO
        ).pack()

        ctk.CTkLabel(
            cabecalho,
            text="GERADOR EXPERIMENTAL DE TEXTOS",
            font=("Consolas", 11),
            text_color=SECUNDARIO
        ).pack(pady=(6, 0))

        # Painel de configurações
        configuracoes = ctk.CTkFrame(
            self,
            fg_color=PAINEL,
            corner_radius=16
        )
        configuracoes.pack(fill="x", padx=35, pady=10)

        ctk.CTkLabel(
            configuracoes,
            text="01  —  ESCOLHA O MODO",
            text_color=DOURADO,
            font=("Consolas", 13, "bold")
        ).pack(anchor="w", padx=22, pady=(20, 10))

        modos_frame = ctk.CTkFrame(
            configuracoes,
            fg_color="transparent"
        )
        modos_frame.pack(fill="x", padx=18)

        for modo, descricao in [
            ("caotico", "Caótico"),
            ("poetico", "Poético"),
            ("cientifico", "Científico"),
        ]:
            ctk.CTkRadioButton(
                modos_frame,
                text=descricao,
                variable=self.modo_selecionado,
                value=modo,
                text_color=TEXTO,
                fg_color=DOURADO,
                hover_color="#A88A5D",
                border_color=SECUNDARIO,
                font=("Segoe UI", 13)
            ).pack(side="left", expand=True, padx=5, pady=8)

        # Semente
        ctk.CTkLabel(
            configuracoes,
            text="02  —  SEMENTE",
            text_color=DOURADO,
            font=("Consolas", 13, "bold")
        ).pack(anchor="w", padx=22, pady=(20, 8))

        semente_frame = ctk.CTkFrame(
            configuracoes,
            fg_color="transparent"
        )
        semente_frame.pack(fill="x", padx=22)

        self.campo_semente = ctk.CTkEntry(
            semente_frame,
            textvariable=self.semente,
            placeholder_text="Ex.: 20261029 (vazio = aleatória)",
            height=38,
            fg_color=FUNDO,
            border_color="#48444D",
            text_color=TEXTO
        )
        self.campo_semente.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ctk.CTkButton(
            semente_frame,
            text="Randomizar",
            command=self.randomizar_semente,
            width=115,
            height=38,
            fg_color="#39303F",
            hover_color="#51405A",
            text_color=TEXTO
        ).pack(side="right")

        # Quantidade de palavras
        ctk.CTkLabel(
            configuracoes,
            text="03  —  QUANTIDADE DE PALAVRAS",
            text_color=DOURADO,
            font=("Consolas", 13, "bold")
        ).pack(anchor="w", padx=22, pady=(20, 0))

        quantidade_frame = ctk.CTkFrame(
            configuracoes,
            fg_color="transparent"
        )
        quantidade_frame.pack(
            fill="x",
            padx=22,
            pady=(5, 0)
        )

        self.rotulo_quantidade = ctk.CTkLabel(
            quantidade_frame,
            text="30 palavras",
            text_color=TEXTO,
            font=("Segoe UI", 14, "bold")
        )
        self.rotulo_quantidade.pack(side="right")

        self.controle_quantidade = ctk.CTkSlider(
            configuracoes,
            from_=5,
            to=120,
            number_of_steps=115,
            variable=self.quantidade,
            command=self.atualizar_quantidade,
            progress_color=DOURADO,
            button_color=DOURADO,
            button_hover_color="#E0C18D"
        )
        self.controle_quantidade.pack(
            fill="x",
            padx=24,
            pady=(8, 20)
        )

        # Botão de geração
        ctk.CTkButton(
            self,
            text="✦   GERAR TEXTO",
            command=self.gerar_texto,
            height=46,
            corner_radius=10,
            fg_color=DOURADO,
            hover_color="#A88A5D",
            text_color="#211B15",
            font=("Segoe UI", 14, "bold")
        ).pack(fill="x", padx=35, pady=(12, 18))

        # Área de resultado
        resultado_cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        resultado_cabecalho.pack(
            fill="x",
            padx=35,
            pady=(0, 8)
        )

        ctk.CTkLabel(
            resultado_cabecalho,
            text="FRAGMENTO GERADO",
            text_color=DOURADO,
            font=("Consolas", 13, "bold")
        ).pack(side="left")

        self.rotulo_total = ctk.CTkLabel(
            resultado_cabecalho,
            text="0 palavras",
            text_color=SECUNDARIO,
            font=("Segoe UI", 11)
        )
        self.rotulo_total.pack(side="right")

        self.resultado = ctk.CTkTextbox(
            self,
            height=180,
            corner_radius=12,
            fg_color=PAINEL,
            border_width=1,
            border_color="#39343D",
            text_color=TEXTO,
            font=("Georgia", 16),
            wrap="word"
        )
        self.resultado.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 12)
        )

        self.resultado.insert(
            "1.0",
            "As páginas aguardam. Escolha um modo e gere seu primeiro texto."
        )
        self.resultado.configure(state="disabled")

        # Rodapé
        ctk.CTkLabel(
            self,
            text="BIBLIOTECA DE BABEL  •  EXPERIMENTO EM PYTHON",
            text_color="#71685C",
            font=("Consolas", 10)
        ).pack(pady=(0, 15))

    def atualizar_quantidade(self, valor):
        quantidade = round(valor)
        self.quantidade.set(quantidade)
        self.rotulo_quantidade.configure(
            text=f"{quantidade} palavras"
        )

    def randomizar_semente(self):
        self.semente.set(str(random.randint(0, 999999999)))

    def gerar_texto(self):
        try:
            quantidade = self.quantidade.get()
            valor_semente = self.semente.get().strip()

            if not 5 <= quantidade <= 120:
                messagebox.showerror(
                    "Quantidade inválida",
                    "Escolha entre 5 e 120 palavras."
                )
                return

            if valor_semente:
                try:
                    semente = int(valor_semente)
                except ValueError:
                    messagebox.showerror(
                        "Semente inválida",
                        "A semente deve ser um número inteiro."
                    )
                    return
            else:
                semente = random.randint(0, 999999999)
                self.semente.set(str(semente))

            geradores = {
                "caotico": gerar_texto_caotico,
                "poetico": gerar_texto_poetico,
                "cientifico": gerar_texto_cientifico,
            }

            gerador = geradores[self.modo_selecionado.get()]

            texto = gerador(
                self.vocabulario,
                quantidade,
                semente
            )

            self.resultado.configure(state="normal")
            self.resultado.delete("1.0", "end")
            self.resultado.insert("1.0", texto)
            self.resultado.configure(state="disabled")

            total = len(texto.split())
            self.rotulo_total.configure(
                text=f"{total} palavras geradas"
            )

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as erro:
            messagebox.showerror(
                "Erro ao gerar texto",
                str(erro)
            )


def iniciar_interface():
    app = BibliotecaDeBabel()
    app.mainloop()


if __name__ == "__main__":
    iniciar_interface()
