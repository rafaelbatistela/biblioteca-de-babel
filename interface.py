import json
import random
import tkinter as tk
from tkinter import messagebox
import webbrowser

import customtkinter as ctk

from modos.caotico import gerar_texto_caotico
from modos.poetico import gerar_texto_poetico
from modos.cientifico import gerar_texto_cientifico
from main import carregar_vocabulario


# Configuração visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Paleta de Cores — Biblioteca de Mogno e Livros Antigos
FUNDO = "#14100E"          # Espresso escuro / madeira profunda
PAINEL = "#211A16"         # Tom de madeira nobre (Mogno/Nogueira)
PAINEL_CARD = "#2B231E"    # Fundo dos cards de modo
PAINEL_CARD_HOVER = "#352B24" 
PAINEL_INTERNO = "#1A1310" # Fundo para caixas de texto e entradas
DOURADO = "#C59B27"        # Ouro envelhecido / Cobre clássico
DOURADO_HOVER = "#DCAE3D"
TEXTO = "#F4EBD9"          # Papel envelhecido (creme)
SECUNDARIO = "#A69279"     # Bronze suave / Tinta desbotada
BORDA_SUTIL = "#3D312A"    # Divisores discretos em tons de terra


class BibliotecaDeBabel(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Biblioteca de Babel — Gerador Experimental")
        self.geometry("940x840")
        self.minsize(760, 720)
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
        cabecalho.pack(fill="x", padx=40, pady=(25, 15))

        ctk.CTkLabel(
            cabecalho,
            text="ℬIBLIOTECA DE BABEL",
            font=("Georgia", 26, "bold"),
            text_color=DOURADO
        ).pack(anchor="w")

        ctk.CTkLabel(
            cabecalho,
            text="SISTEMA EXPERIMENTAL DE SÍNTESE TEXTUAL  •  BORGES",
            font=("Consolas", 10),
            text_color=SECUNDARIO
        ).pack(anchor="w", pady=(3, 0))

        # Painel principal
        configuracoes = ctk.CTkFrame(
            self,
            fg_color=PAINEL,
            corner_radius=16,
            border_width=1,
            border_color=BORDA_SUTIL
        )
        configuracoes.pack(fill="x", padx=40, pady=5)

        # Seção 01 — Modos em Cartões Maiores
        ctk.CTkLabel(
            configuracoes,
            text="01  —  ESCOLHA O MODO DE MANUSCRITO",
            text_color=DOURADO,
            font=("Consolas", 11, "bold")
        ).pack(anchor="w", padx=25, pady=(20, 12))

        modos_frame = ctk.CTkFrame(
            configuracoes,
            fg_color="transparent"
        )
        modos_frame.pack(fill="x", padx=20, pady=(0, 5))

        # Dados dos modos para os cartões
        dados_modos = [
            ("caotico", "Caótico", "Embaralha vocábulos e estruturas sem rigor gramatical, gerando colagens imprevisíveis."),
            ("poetico", "Poético", "Conecta imagens líricas, cadência rítmica e ressonância emocional com foco estético."),
            ("cientifico", "Científico", "Simula tratados formais, terminologias técnicas e um aparente rigor acadêmico.")
        ]

        for modo, titulo, desc in dados_modos:
            card = ctk.CTkFrame(
                modos_frame,
                fg_color=PAINEL_CARD,
                corner_radius=10,
                border_width=1,
                border_color=BORDA_SUTIL
            )
            card.pack(side="left", expand=True, fill="both", padx=6, pady=5)

            # Radiobutton dentro do card
            rb = ctk.CTkRadioButton(
                card,
                text=titulo,
                variable=self.modo_selecionado,
                value=modo,
                text_color=TEXTO,
                fg_color=DOURADO,
                hover_color=DOURADO_HOVER,
                border_color=SECUNDARIO,
                font=("Georgia", 14, "bold")
            )
            rb.pack(anchor="w", padx=15, pady=(15, 5))

            # Descrição do modo
            lbl_desc = ctk.CTkLabel(
                card,
                text=desc,
                text_color=SECUNDARIO,
                font=("Segoe UI", 11),
                wraplength=220,
                justify="left"
            )
            lbl_desc.pack(anchor="w", padx=15, pady=(0, 15))

        # Seção 02 — Semente
        ctk.CTkLabel(
            configuracoes,
            text="02  —  SEMENTE DO LABIRINTO (SEED)",
            text_color=DOURADO,
            font=("Consolas", 11, "bold")
        ).pack(anchor="w", padx=25, pady=(18, 8))

        semente_frame = ctk.CTkFrame(
            configuracoes,
            fg_color="transparent"
        )
        semente_frame.pack(fill="x", padx=25)

        self.campo_semente = ctk.CTkEntry(
            semente_frame,
            textvariable=self.semente,
            placeholder_text="Ex.: 20261029 (vazio = aleatória)",
            height=38,
            fg_color=PAINEL_INTERNO,
            border_width=1,
            border_color=BORDA_SUTIL,
            text_color=TEXTO,
            font=("Consolas", 12)
        )
        self.campo_semente.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12)
        )

        ctk.CTkButton(
            semente_frame,
            text="🎲  Sortear",
            command=self.randomizar_semente,
            width=115,
            height=38,
            fg_color="#2E231D",
            hover_color="#403229",
            text_color=TEXTO,
            font=("Segoe UI", 12, "bold")
        ).pack(side="right")

        # Seção 03 — Quantidade de palavras
        ctk.CTkLabel(
            configuracoes,
            text="03  —  QUANTIDADE DE PALAVRAS",
            text_color=DOURADO,
            font=("Consolas", 11, "bold")
        ).pack(anchor="w", padx=25, pady=(18, 0))

        quantidade_frame = ctk.CTkFrame(
            configuracoes,
            fg_color="transparent"
        )
        quantidade_frame.pack(
            fill="x",
            padx=25,
            pady=(2, 0)
        )

        self.rotulo_quantidade = ctk.CTkLabel(
            quantidade_frame,
            text="30 palavras",
            text_color=TEXTO,
            font=("Consolas", 12, "bold")
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
            button_hover_color=DOURADO_HOVER,
            height=16
        )
        self.controle_quantidade.pack(
            fill="x",
            padx=27,
            pady=(6, 20)
        )

        # Botão principal de geração
        ctk.CTkButton(
            self,
            text="✦   EXTRAIR MANUSCRITO DA BIBLIOTECA",
            command=self.gerar_texto,
            height=44,
            corner_radius=10,
            fg_color=DOURADO,
            hover_color=DOURADO_HOVER,
            text_color="#14100E",
            font=("Segoe UI", 13, "bold")
        ).pack(fill="x", padx=40, pady=(12, 12))

        # Área de resultado
        resultado_cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        resultado_cabecalho.pack(
            fill="x",
            padx=40,
            pady=(0, 4)
        )

        ctk.CTkLabel(
            resultado_cabecalho,
            text="FRAGMENTO DECIFRADO",
            text_color=DOURADO,
            font=("Consolas", 11, "bold")
        ).pack(side="left")

        self.rotulo_total = ctk.CTkLabel(
            resultado_cabecalho,
            text="0 palavras",
            text_color=SECUNDARIO,
            font=("Consolas", 11)
        )
        self.rotulo_total.pack(side="right")

        self.resultado = ctk.CTkTextbox(
            self,
            height=130,
            corner_radius=10,
            fg_color=PAINEL,
            border_width=1,
            border_color=BORDA_SUTIL,
            text_color=TEXTO,
            font=("Georgia", 14),
            wrap="word",
            padx=12,
            pady=12
        )
        self.resultado.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 10)
        )

        self.resultado.insert(
            "1.0",
            "As prateleiras infindáveis aguardam... Selecione um modo e extraia seu fragmento."
        )
        self.resultado.configure(state="disabled")

        # Rodapé com Aviso de Experimento e Links Sociais
        rodape_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        rodape_frame.pack(fill="x", padx=40, pady=(0, 15))

        ctk.CTkLabel(
            rodape_frame,
            text="⚠️ Experimento de randomização de palavras. Não tome nenhum fragmento gerado como verdade absoluta.",
            text_color=SECUNDARIO,
            font=("Consolas", 9)
        ).pack(anchor="w")

        links_frame = ctk.CTkFrame(
            rodape_frame,
            fg_color="transparent"
        )
        links_frame.pack(fill="x", pady=(4, 0))

        ctk.CTkLabel(
            links_frame,
            text="Desenvolvido por Rafael Batistela  •",
            text_color=SECUNDARIO,
            font=("Consolas", 9)
        ).pack(side="left")

        btn_ig = ctk.CTkButton(
            links_frame,
            text="Instagram",
            command=lambda: webbrowser.open("https://www.instagram.com/batis_rafael/"),
            fg_color="transparent",
            text_color=DOURADO,
            hover_color="#2B231E",
            font=("Consolas", 9, "underline"),
            width=60,
            height=20
        )
        btn_ig.pack(side="left", padx=2)

        ctk.CTkLabel(
            links_frame,
            text="•",
            text_color=SECUNDARIO,
            font=("Consolas", 9)
        ).pack(side="left", padx=2)

        btn_git = ctk.CTkButton(
            links_frame,
            text="GitHub",
            command=lambda: webbrowser.open("https://github.com/rafaelbatistela"),
            fg_color="transparent",
            text_color=DOURADO,
            hover_color="#2B231E",
            font=("Consolas", 9, "underline"),
            width=50,
            height=20
        )
        btn_git.pack(side="left")

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