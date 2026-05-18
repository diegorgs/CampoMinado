import pygame
from core.tabuleiro import Tabuleiro

class JogoCampoMinado:
    def __init__(self, linhas=9, colunas=9, minas=10, tamanho_celula=40):
        pygame.init()
        pygame.display.set_caption('Campo Minado')
        
        self.linhas = linhas
        self.colunas = colunas
        self.tamanho_celula = tamanho_celula
        
        self.largura = colunas * tamanho_celula
        self.altura = linhas * tamanho_celula
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        
        self.cores = {
            'preto': (0, 0, 0),
            'vermelho': (255, 0, 0),
            'cinza_claro': (200, 200, 200),
            'cinza_medio': (150, 150, 150),
            'cinza_escuro': (100, 100, 100),
            'branco': (255, 255, 255),
            'verde': (0, 255, 0),
            'azul': (0, 0, 255)
        }
        
        self.fonte = pygame.font.SysFont(None, 30)
        self.tabuleiro = Tabuleiro(linhas, colunas, minas)
        self.fim_jogo = False
        self.vitoria = False

    def desenhar(self):
        self.tela.fill(self.cores['cinza_claro'])
        
        for i in range(self.linhas):
            for j in range(self.colunas):
                x = j * self.tamanho_celula
                y = i * self.tamanho_celula
                
                celula = self.tabuleiro.grid[i][j]
                
                rect = (x, y, self.tamanho_celula, self.tamanho_celula)
                
                if celula.revelada:
                    pygame.draw.rect(self.tela, self.cores['cinza_claro'], rect)
                    pygame.draw.rect(self.tela, self.cores['preto'], rect, 1)
                    
                    if celula.tem_mina:
                        # Desenha uma mina
                        pygame.draw.circle(self.tela, self.cores['vermelho'], 
                                           (x + self.tamanho_celula//2, y + self.tamanho_celula//2), 
                                           self.tamanho_celula//3)
                    elif celula.minas_vizinhas > 0:
                        # Desenha o número de minas
                        texto = self.fonte.render(str(celula.minas_vizinhas), True, self.cores['preto'])
                        texto_rect = texto.get_rect(center=(x + self.tamanho_celula//2, y + self.tamanho_celula//2))
                        self.tela.blit(texto, texto_rect)
                else:
                    pygame.draw.rect(self.tela, self.cores['cinza_medio'], rect)
                    pygame.draw.rect(self.tela, self.cores['preto'], rect, 1)
                    
                    if celula.marcada:
                        # Desenha uma bandeira
                        centro_x, centro_y = x + self.tamanho_celula//2, y + self.tamanho_celula//2
                        pygame.draw.circle(self.tela, self.cores['azul'], (centro_x, centro_y), self.tamanho_celula//4)
        
        # Desenha a mensagem de fim de jogo por cima
        if self.fim_jogo:
            mensagem = "Você Venceu!" if self.vitoria else "Você Perdeu!"
            cor_msg = self.cores['verde'] if self.vitoria else self.cores['vermelho']
            texto_fim = self.fonte.render(mensagem, True, cor_msg)
            
            fundo_msg = pygame.Surface((self.largura, 40))
            fundo_msg.fill(self.cores['preto'])
            self.tela.blit(fundo_msg, (0, self.altura // 2 - 20))
            
            texto_rect = texto_fim.get_rect(center=(self.largura // 2, self.altura // 2))
            self.tela.blit(texto_fim, texto_rect)

        pygame.display.update()

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.MOUSEBUTTONDOWN and not self.fim_jogo:
                x, y = pygame.mouse.get_pos()
                j = x // self.tamanho_celula
                i = y // self.tamanho_celula
                
                if not (0 <= i < self.linhas and 0 <= j < self.colunas):
                    continue

                if evento.button == 1:  # Botão esquerdo
                    if not self.tabuleiro.grid[i][j].marcada:
                        self.tabuleiro.revelar(i, j)
                        if self.tabuleiro.grid[i][j].tem_mina:
                            self.fim_jogo = True
                            self.vitoria = False
                            self._revelar_todas_minas()
                        elif self.tabuleiro.verificar_vitoria():
                            self.fim_jogo = True
                            self.vitoria = True
                
                elif evento.button == 3:  # Botão direito
                    self.tabuleiro.alternar_marca(i, j)
                    
        return True

    def _revelar_todas_minas(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.tabuleiro.grid[i][j].tem_mina:
                    self.tabuleiro.grid[i][j].revelada = True

    def executar(self):
        rodando = True
        relogio = pygame.time.Clock()
        
        while rodando:
            rodando = self.processar_eventos()
            self.desenhar()
            relogio.tick(30)
            
        pygame.quit()