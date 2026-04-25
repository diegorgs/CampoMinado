# configurações iniciais:
import pygame
import random

pygame.init()
pygame.display.set_caption('Campo Minado')
largura, altura = 360, 360
tela = pygame.display.set_mode((largura, altura))

# cores
preto = (0, 0, 0)
vermelho = (255, 0, 0)
cinza_claro = (200, 200, 200)
cinza_medio = (150, 150, 150)
cinza_escuro = (100, 100, 100)

# paramentros:

linhas = 9
colunas = 9
bombas = 2
tamanho_celula = 40

class Celula:
    def __init__(self):
        self.tem_bomba = False
        self.revelada = False
        self.bandeira = False
        self.numero = 0

tabuleiro = []

for i in range(linhas):
    linha = []
    for j in range(colunas):
        linha.append(Celula())
    tabuleiro.append(linha)

# def desenhar_tabuleiro():
#     for i in range(linhas):
#         for j in range(colunas):
#             x = j * tamanho_celula
#             y = i * tamanho_celula

#             pygame.draw.rect(tela, cinza_medio, (x, y, tamanho_celula, tamanho_celula))
#             pygame.draw.rect(tela, preto, (x, y, tamanho_celula, tamanho_celula), 1)

def desenhar_tabuleiro():
    for i in range(linhas):
        for j in range(colunas):
            x = j * tamanho_celula
            y = i * tamanho_celula

            celula = tabuleiro[i][j]

            if celula.revelada:
                pygame.draw.rect(tela, cinza_claro, (x, y, tamanho_celula, tamanho_celula))

                if celula.tem_bomba:
                    pygame.draw.circle(tela, vermelho, (x + 20, y + 20), 10)
                elif celula.numero > 0:
                    fonte = pygame.font.SysFont(None, 24)
                    texto = fonte.render(str(celula.numero), True, preto)
                    tela.blit(texto, (x + 15, y + 10))
            else:
                pygame.draw.rect(tela, cinza_medio, (x, y, tamanho_celula, tamanho_celula))

            pygame.draw.rect(tela, preto, (x, y, tamanho_celula, tamanho_celula), 1)


def rodar_jogo():
    fim_jogo = False
    relogio = pygame.time.Clock()
    
    while not fim_jogo:
        tela.fill(cinza_claro)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                 fim_jogo = True
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                coluna = x_mouse // tamanho_celula
                linha = y_mouse // tamanho_celula

                # evita erro ao clicar fora do tabuleiro
                if 0 <= linha < linhas and 0 <= coluna < colunas:
                    celula = tabuleiro[linha][coluna]

                    # botão esquerdo → revelar
                    if evento.button == 1:
                        celula.revelada = True

                        if celula.tem_bomba:
                            print("💥 Game Over")
                            fim_jogo = True  # encerra o jogo

                    # botão direito → bandeira
                    elif evento.button == 3:
                        if not celula.revelada:
                            celula.bandeira = not celula.bandeira

        desenhar_tabuleiro()
        pygame.display.update()
        relogio.tick(30)

    pygame.quit()
# criar um loop infinito:

# desenhar os objetos do jogo na tela:
# tabuleiro
# células
# bombas
def distribuir_bombas():
    bombas_colocadas = 0

    while bombas_colocadas < bombas:
        linha_aleatoria = random.randrange(linhas)
        coluna_aleatoria = random.randrange(colunas)

        celula = tabuleiro[linha_aleatoria][coluna_aleatoria]

        if not celula.tem_bomba:
                celula.tem_bomba = True
                bombas_colocadas += 1
  


for i in range(linhas):
    for j in range(colunas):
        if tabuleiro[i][j].tem_bomba:
            print('Bomba em:', i, j)


def calcular_numeros():
    for i in range(linhas):
        for j in range(colunas):
            contador = 0

            for x in range(i-1, i+2):
                for y in range(j-1, j+2):

                    if 0 <= x < linhas and 0 <= y < colunas:
                        if x == i and y == j:
                            continue
                        if tabuleiro[x][y].tem_bomba:
                            contador += 1

            tabuleiro[i][j].numero = contador

distribuir_bombas()
calcular_numeros()

for i in range(linhas):
    for j in range(colunas):
        if tabuleiro[i][j].tem_bomba:
            print("💣", end=" ")
        else:
            print(tabuleiro[i][j].numero, end=" ")
    print()
# bandeiras

# criar a lógica de terminar o jogo:
# o que acontece:
# usuário escolheu a bomba
# usuário abriu todas as células

# pegar a interações do usuário:
# fechou a tela
# apertou com o mouse esquerdo para abrir uma célula 
# apertou com o mouse direto para colocar uma bandeira 

rodar_jogo()
