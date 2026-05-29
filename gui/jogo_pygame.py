import pygame
from core.tabuleiro import Tabuleiro

class JogoCampoMinado:
    def __init__(self, linhas=9, colunas=9, minas=10, tamanho_celula=40, altura_hud=50):
        pygame.init()
        pygame.display.set_caption('Campo Minado')
        
        self.linhas = linhas
        self.colunas = colunas
        self.minas = minas
        self.tamanho_celula = tamanho_celula
        self.altura_hud = altura_hud
        self.tempo_inicial = pygame.time.get_ticks()
        
        self.largura = colunas * tamanho_celula
        self.altura = linhas * tamanho_celula + self.altura_hud
        self.tela = pygame.display.set_mode((self.largura, self.altura))

        self.estado = "menu"
        

        self.cores = {
            'preto': (0, 0, 0),
            'vermelho': (255, 0, 0),
            'cinza_claro': (200, 200, 200),
            'cinza_medio': (150, 150, 150),
            'cinza_escuro': (100, 100, 100),
            'branco': (255, 255, 255),
            'verde': (0, 255, 0),
            'azul': (0, 0, 255),
            'azul_escuro': (0, 0, 139),
            'laranja': (255, 165, 0),
            'verde_classico': (0, 128, 0),
        }
        
        self.cores_numeros = {
            1: self.cores['azul'],
            2: self.cores['verde_classico'],
            3: self.cores['vermelho'],
            4: self.cores['azul_escuro'],
            5: self.cores['laranja']}
        
        self.mina_img = pygame.image.load("assets/mina.png")
        self.mina_img = pygame.transform.scale(
        self.mina_img,(30, 30))
        
        self.mina_hud_img = pygame.transform.scale(
        self.mina_img,(30, 30))

        self.bandeira_img = pygame.image.load("assets/flags.png")
        self.bandeira_img = pygame.transform.scale(
        self.bandeira_img,(30, 30))

        self.relogio_img = pygame.image.load("assets/relogio.png")
        self.relogio_img = pygame.transform.scale(
        self.relogio_img,(30, 30))

        
        self.fonte = pygame.font.SysFont(None, 30)
        self.tabuleiro = Tabuleiro(linhas, colunas, minas)
        self.fim_jogo = False
        self.vitoria = False
        self.estado = "menu"

    def desenhar(self):
        self.tela.fill(self.cores['cinza_claro'])

        if self.estado == "menu":
            self.tela.fill(self.cores['cinza_escuro'])
            titulo = self.fonte.render("CAMPO MINADO", True, self.cores['branco'])
            self.tela.blit(titulo, (60, 50))

            opcao1 = self.fonte.render("1 - Iniciante",True,self.cores['branco'])
            opcao2 = self.fonte.render("2 - Dificil",True,self.cores['branco'])
            opcao3 = self.fonte.render("3 - Impossivel",True,self.cores['branco'])

            self.tela.blit(opcao1, (60, 120))
            self.tela.blit(opcao2, (60, 170))
            self.tela.blit(opcao3, (60, 220))

            pygame.display.update()
            return

        pygame.draw.rect(self.tela, self.cores['cinza_escuro'],(0, 0, self.largura, self.altura_hud))
        tempo_atual = pygame.time.get_ticks()
        tempo_segundos = (tempo_atual - self.tempo_inicial) // 1000

        texto_tempo = self.fonte.render(f"{tempo_segundos}",True,self.cores['branco'])

        self.tela.blit(self.relogio_img, (255, 5))
        self.tela.blit(texto_tempo, (300, 10))

        bandeiras = 0

        for i in range(self.linhas):
            for j in range(self.colunas):
            
                if self.tabuleiro.grid[i][j].marcada:
                    bandeiras += 1

        minas_restantes = self.minas - bandeiras

        texto_minas = self.fonte.render(f"{minas_restantes}", True, self.cores['branco'])

        self.tela.blit(self.mina_hud_img, (10, 6))
        self.tela.blit(texto_minas, (40, 10))

        for i in range(self.linhas):
            for j in range(self.colunas):
                x = j * self.tamanho_celula
                y = self.altura_hud + (i * self.tamanho_celula)
                
                celula = self.tabuleiro.grid[i][j]
                
                rect = (x, y, self.tamanho_celula, self.tamanho_celula)
                
                if celula.revelada:
                    pygame.draw.rect(self.tela, self.cores['cinza_claro'], rect)
                    pygame.draw.rect(self.tela, self.cores['preto'], rect, 1)
                    
                    if celula.tem_mina:
                        # Desenha uma mina
                        self.tela.blit(self.mina_img, (x + 5, y + 5))
                    elif celula.minas_vizinhas > 0:
                        # Desenha o número de minas
                        texto = self.fonte.render(str(celula.minas_vizinhas), True, self.cores_numeros[celula.minas_vizinhas])
                        texto_rect = texto.get_rect(center=(x + self.tamanho_celula//2, y + self.tamanho_celula//2))
                        self.tela.blit(texto, texto_rect)
                else:
                    pygame.draw.rect(self.tela, self.cores['cinza_medio'], rect)
                    pygame.draw.line(self.tela, self.cores['branco'],(x, y), (x + self.tamanho_celula, y),2)
                    pygame.draw.line(self.tela, self.cores['branco'],(x, y), (x, y + self.tamanho_celula),2)
                    pygame.draw.line(self.tela, self.cores['cinza_escuro'], (x, y + self.tamanho_celula), (x + self.tamanho_celula, y + self.tamanho_celula),2)
                    pygame.draw.line(self.tela, self.cores['cinza_escuro'], (x + self.tamanho_celula, y), (x + self.tamanho_celula, y + self.tamanho_celula),2)
                    pygame.draw.rect(self.tela, self.cores['preto'], rect, 1)
                    
                    if celula.marcada:
                        # Desenha uma bandeira
                        centro_x, centro_y = x + self.tamanho_celula//2, y + self.tamanho_celula//2
                        self.tela.blit(self.bandeira_img, (x + 5, y + 5))
        
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
                i = (y - self.altura_hud) // self.tamanho_celula
                
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

            if evento.type == pygame.KEYDOWN:

                if self.estado == "menu":
                    if evento.key == pygame.K_1:
                        self.estado = "jogo"
                        self.tabuleiro = Tabuleiro(
                        self.linhas,
                        self.colunas,
                        self.minas)

                        self.largura = self.colunas * self.tamanho_celula
                        self.altura = (self.linhas * self.tamanho_celula + self.altura_hud)

                        self.tela = pygame.display.set_mode((self.largura, self.altura))

                        
                    if evento.key == pygame.K_2:
                        self.estado = "jogo"
                        self.linhas = 16 
                        self.colunas = 16
                        self.minas = 40
                        self.tabuleiro = Tabuleiro(
                        self.linhas,
                        self.colunas,
                        self.minas)
                        self.bandeira_img = pygame.transform.scale(self.bandeira_img,(30, 30))
                        self.mina_img = pygame.transform.scale(self.mina_img,(30, 30))
                        self.largura = self.colunas * self.tamanho_celula
                        self.altura = (self.linhas * self.tamanho_celula + self.altura_hud)

                        self.tela = pygame.display.set_mode((self.largura, self.altura))


                    if evento.key == pygame.K_3:
                        self.estado = "jogo"
                        self.linhas = 24 
                        self.colunas = 24
                        self.minas = 120
                        self.tabuleiro = Tabuleiro(
                        self.linhas,
                        self.colunas,
                        self.minas)
                        self.tamanho_celula = 25
                        self.bandeira_img = pygame.transform.scale(self.bandeira_img,(20, 20))
                        self.mina_img = pygame.transform.scale(self.mina_img,(18, 18))
                        self.largura = self.colunas * self.tamanho_celula
                        self.altura = (self.linhas * self.tamanho_celula + self.altura_hud)

                        self.tela = pygame.display.set_mode((self.largura, self.altura))
                
                if evento.key == pygame.K_r:
                    if evento.key == pygame.K_r:
                        self.tabuleiro = Tabuleiro(
                        self.linhas,
                        self.colunas,
                        self.minas)

                        self.largura = self.colunas * self.tamanho_celula
                        self.altura = ( self.linhas * self.tamanho_celula + self.altura_hud)

                        self.tela = pygame.display.set_mode((self.largura, self.altura))

                        
                        self.fim_jogo = False
                        self.vitoria = False
                        self.tempo_inicial = pygame.time.get_ticks()

                
                if evento.key == pygame.K_ESCAPE:
                    self.estado = "menu"
                    self.linhas = 9
                    self.colunas = 9
                    self.minas = 10
                    self.tamanho_celula = 40

                    self.largura = self.colunas * self.tamanho_celula
                    self.altura = ( self.linhas * self.tamanho_celula + self.altura_hud)

                    self.tela = pygame.display.set_mode((self.largura, self.altura))

                    
                    self.fim_jogo = False
                    self.vitoria = False
                    self.tempo_inicial = pygame.time.get_ticks()

                
                if evento.key == pygame.K_q:
                    pygame.quit()

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