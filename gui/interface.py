import tkinter as tk
from core.tabuleiro import Tabuleiro


class CampoMinadoGUI:
    def __init__(self, root, linhas=8, colunas=8, minas=10):
        self.root = root
        self.tabuleiro = Tabuleiro(linhas, colunas, minas)
        self.botoes = []

        self.frame = tk.Frame(root)
        self.frame.pack()

        self._criar_botoes()

    def _criar_botoes(self):
        for i in range(self.tabuleiro.linhas):
            linha = []
            for j in range(self.tabuleiro.colunas):
                btn = tk.Button(self.frame, width=3, height=1,
                                command=lambda i=i, j=j: self.clique(i, j))
                btn.grid(row=i, column=j)
                linha.append(btn)
            self.botoes.append(linha)

    def clique(self, i, j):
        celula = self.tabuleiro.grid[i][j]

        if celula.tem_mina:
            print("💥 Perdeu!")
            return

        self.tabuleiro.revelar(i, j)
        self._atualizar()

    def _atualizar(self):
        for i in range(self.tabuleiro.linhas):
            for j in range(self.tabuleiro.colunas):
                c = self.tabuleiro.grid[i][j]
                btn = self.botoes[i][j]

                if c.revelada:
                    btn.config(text=str(c.minas_vizinhas or ""), bg="lightgrey")