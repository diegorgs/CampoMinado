import random
from core.celula import Celula


class Tabuleiro:
    def __init__(self, linhas, colunas, minas):
        self.linhas = linhas
        self.colunas = colunas
        self.minas = minas

        self.grid = [[Celula() for _ in range(colunas)] for _ in range(linhas)]
        self.primeiro_clique = True

    def _posicionar_minas(self, i_excluido, j_excluido):
        posicoes_validas = []
        for i in range(self.linhas):
            for j in range(self.colunas):
                # Ignora a célula clicada e vizinhos para garantir espaço vazio no 1º clique
                if abs(i - i_excluido) <= 1 and abs(j - j_excluido) <= 1:
                    continue
                posicoes_validas.append((i, j))
                
        # Fallback caso o tabuleiro seja muito pequeno para a quantidade de minas
        if len(posicoes_validas) < self.minas:
            posicoes_validas = [(i, j) for i in range(self.linhas) for j in range(self.colunas) if (i, j) != (i_excluido, j_excluido)]

        posicoes = random.sample(posicoes_validas, self.minas)
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

        if self.primeiro_clique:
            self.primeiro_clique = False
            self._posicionar_minas(i, j)
            self._calcular_vizinhos()

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

    def alternar_marca(self, i, j):
        if not (0 <= i < self.linhas and 0 <= j < self.colunas):
            return
            
        celula = self.grid[i][j]
        if not celula.revelada:
            celula.marcada = not celula.marcada

    def verificar_vitoria(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                celula = self.grid[i][j]
                if not celula.tem_mina and not celula.revelada:
                    return False
        return True