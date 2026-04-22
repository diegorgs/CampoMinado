import random
from core.celula import Celula


class Tabuleiro:
    def __init__(self, linhas, colunas, minas):
        self.linhas = linhas
        self.colunas = colunas
        self.minas = minas

        self.grid = [[Celula() for _ in range(colunas)] for _ in range(linhas)]

        self._posicionar_minas()
        self._calcular_vizinhos()

    def _posicionar_minas(self):
        posicoes = random.sample(
            [(i, j) for i in range(self.linhas) for j in range(self.colunas)],
            self.minas
        )
        for i, j in posicoes:
            self.grid[i][j].tem_mina = True

    def _calcular_vizinhos(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.grid[i][j].tem_mina:
                    continue

                count = 0
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        if 0 <= x < self.linhas and 0 <= y < self.colunas:
                            if self.grid[x][y].tem_mina:
                                count += 1

                self.grid[i][j].minas_vizinhas = count
                
    def revelar(self, i, j):
        if not (0 <= i < self.linhas and 0 <= j < self.colunas):
            return

        celula = self.grid[i][j]

        if celula.revelada or celula.marcada:
            return

        celula.revelada = True

        # Se não tiver minas ao redor, revela vizinhos
        if celula.minas_vizinhas == 0 and not celula.tem_mina:
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):
                    if 0 <= x < self.linhas and 0 <= y < self.colunas:
                        self.revelar(x, y)