import pygame
from core import sons
from core.tabuleiro import Tabuleiro

# Interface do jogo Campo Minado usando Pygame.
# Esta classe controla o menu, o estado da partida e a renderização do tabuleiro.
class JogoCampoMinado:
    def __init__(self, linhas=9, colunas=9, minas=10, tamanho_celula=40, altura_hud=50):
        # Inicializa o Pygame e seta o título da janela.
        pygame.init()
        pygame.display.set_caption('Campo Minado')
        
        # Configurações de jogo e tamanho inicial do tabuleiro.
        self.linhas = linhas
        self.colunas = colunas
        self.minas = minas
        self.tamanho_celula = tamanho_celula

        # Parâmetros específicos do menu para uma tela maior e botões maiores.
        self.menu_tamanho_celula = 60
        self.menu_largura = 720
        self.menu_altura = 640
        self.altura_hud = altura_hud
        
        # Calcula a largura e altura da janela com base no tabuleiro.
        self.largura = colunas * tamanho_celula
        self.altura = linhas * tamanho_celula + self.altura_hud

        # Estado inicial começa no menu.
        self.estado = "menu"
        if self.estado == "menu":
            self.largura = max(self.largura, self.menu_largura)
            self.altura = max(self.altura, self.menu_altura)

        # Cria a janela do jogo.
        self.tela = pygame.display.set_mode((self.largura, self.altura))

        # Paleta de cores reutilizada em toda a interface.
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
            'azul_ciano': (0, 128, 128),
            'roxo': (128, 0, 128),
            'amarelo': (255, 255, 0)
        }
        
        self.cores_numeros = {
            1: self.cores['azul'],
            2: self.cores['verde_classico'],
            3: self.cores['vermelho'],
            4: self.cores['azul_escuro'],
            5: self.cores['laranja'],
            6: self.cores['azul_ciano'],
            7: self.cores['roxo'],
            8: self.cores['amarelo']
            }
        
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

        
        self.fonte = pygame.font.SysFont('consolas', 28)
        self.fonte_titulo = pygame.font.SysFont('consolas', 52, bold=True)
        self.fonte_mini = pygame.font.SysFont('consolas', 18)
        # Opções de dificuldade do menu principal.
        self.menu_opcoes = [
            {'texto': 'Iniciante', 'linhas': 9, 'colunas': 9, 'minas': 10, 'tamanho_celula': 60},
            {'texto': 'Difícil', 'linhas': 16, 'colunas': 16, 'minas': 40, 'tamanho_celula': 50},
            {'texto': 'Impossível', 'linhas': 24, 'colunas': 24, 'minas': 120, 'tamanho_celula': 35},
        ]
        self.hovered_opcao = None

        # Carrega os sprites originais para redimensioná-los de acordo com o tamanho da grade.
        self.mina_img_original = pygame.image.load("assets/mina.png")
        self.bandeira_img_original = pygame.image.load("assets/flags.png")
        self.relogio_img_original = pygame.image.load("assets/relogio.png")
        self._ajustar_assets(self.tamanho_celula)

        # Cria o tabuleiro e inicializa o estado de partida.
        self.tabuleiro = Tabuleiro(linhas, colunas, minas)
        self.fim_jogo = False
        self.vitoria = False
        self.tempo_final = None
        self.estado = "menu"

    def desenhar(self):
        # Renderiza toda a tela conforme o estado atual do jogo.
        self.tela.fill(self.cores['cinza_claro'])

        if self.estado == "menu":
            # Desenha a tela de seleção de dificuldade.
            self.tela.fill((14, 25, 55))
            titulo_texto = self.fonte_titulo.render("CAMPO MINADO", True, self.cores['amarelo'])
            sombra_titulo = self.fonte_titulo.render("CAMPO MINADO", True, self.cores['preto'])
            self.tela.blit(sombra_titulo, (62, 52))
            self.tela.blit(titulo_texto, (60, 50))

            painel = pygame.Rect(40, 130, self.largura - 80, self.altura - 220)
            pygame.draw.rect(self.tela, self.cores['cinza_escuro'], painel, border_radius=20)
            pygame.draw.rect(self.tela, self.cores['cinza_medio'], painel.inflate(-8, -8), border_radius=16)

            botoes = self._calcular_retangulos_menu()
            mouse_pos = pygame.mouse.get_pos()

            for index, opcao in enumerate(self.menu_opcoes):
                botao = botoes[index]
                destaque = botao.collidepoint(mouse_pos)
                cor_fundo = self.cores['azul_ciano'] if destaque else self.cores['azul']
                cor_texto = self.cores['branco']
                pygame.draw.rect(self.tela, cor_fundo, botao, border_radius=14)
                pygame.draw.rect(self.tela, self.cores['branco'], botao, 2, border_radius=14)

                label = self.fonte.render(f"{index + 1} - {opcao['texto']}", True, cor_texto)
                label_rect = label.get_rect(center=botao.center)
                self.tela.blit(label, label_rect)

            instrucoes = self.fonte_mini.render("Clique em um modo ou pressione 1, 2 ou 3 para iniciar.", True, self.cores['branco'])
            self.tela.blit(instrucoes, (60, self.altura - 70))
            informacao = self.fonte_mini.render("Use ESC para voltar ao menu a qualquer momento.", True, self.cores['cinza_claro'])
            self.tela.blit(informacao, (60, self.altura - 40))

            pygame.display.update()
            return

        pygame.draw.rect(self.tela, self.cores['cinza_escuro'],(0, 0, self.largura, self.altura_hud))
        tempo_atual = self.tempo_final if self.fim_jogo and self.tempo_final is not None else pygame.time.get_ticks()
        tempo_segundos = (tempo_atual - self.tempo_inicial) // 1000

        texto_tempo = self.fonte.render(f"{tempo_segundos}s", True, self.cores['branco'])

        self.tela.blit(self.relogio_img, (10, 5))
        self.tela.blit(texto_tempo, (50, 10))

        bandeiras = 0

        for i in range(self.linhas):
            for j in range(self.colunas):
            
                if self.tabuleiro.grid[i][j].marcada:
                    bandeiras += 1

        minas_restantes = self.minas - bandeiras

        texto_minas = self.fonte.render(f"{minas_restantes}", True, self.cores['branco'])

        self.tela.blit(self.mina_hud_img, (160, 6))
        self.tela.blit(texto_minas, (190, 10))

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
        
        # Desenha a mensagem de fim de jogo por cima do tabuleiro.
        if self.fim_jogo:
            mensagem = "Você Venceu!" if self.vitoria else "Você Perdeu!"
            cor_msg = self.cores['verde'] if self.vitoria else self.cores['vermelho']
            texto_fim = self.fonte_titulo.render(mensagem, True, cor_msg)

            # Tela escurecida de overlay para destacar a mensagem.
            overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.tela.blit(overlay, (0, 0))

            # Caixa central para o painel de fim de jogo.
            caixa = pygame.Rect(self.largura // 2 - 220, self.altura // 2 - 170, 440, 340)
            pygame.draw.rect(self.tela, self.cores['cinza_escuro'], caixa, border_radius=20)
            pygame.draw.rect(self.tela, self.cores['branco'], caixa, 3, border_radius=20)

            # Texto principal com a mensagem de vitória/derrota.
            texto_rect = texto_fim.get_rect(center=(self.largura // 2, self.altura // 2 - 80))
            self.tela.blit(texto_fim, texto_rect)

            # Instruções de teclado apresentadas logo abaixo do título.
            instrucoes1 = self.fonte_mini.render("Pressione R para reiniciar", True, self.cores['branco'])
            instrucoes2 = self.fonte_mini.render("Pressione M para voltar ao menu", True, self.cores['branco'])
            instr1_rect = instrucoes1.get_rect(center=(self.largura // 2, self.altura // 2 - 30))
            instr2_rect = instrucoes2.get_rect(center=(self.largura // 2, self.altura // 2 + 0))
            self.tela.blit(instrucoes1, instr1_rect)
            self.tela.blit(instrucoes2, instr2_rect)

            # Exibe o tempo final de partida, se já estiver definido.
            if self.tempo_final is not None:
                tempo_final_segundos = (self.tempo_final - self.tempo_inicial) // 1000
                texto_tempo_final = self.fonte_mini.render(f"Tempo final: {tempo_final_segundos}s", True, self.cores['amarelo'])
                tempo_final_rect = texto_tempo_final.get_rect(center=(self.largura // 2, self.altura // 2 + 40))
                self.tela.blit(texto_tempo_final, tempo_final_rect)

            # Botões de ação do game over: reiniciar ou voltar ao menu.
            botoes = self._calcular_retangulos_game_over()
            texto_reiniciar = self.fonte.render("REINICIAR", True, self.cores['branco'])
            texto_menu = self.fonte.render("MENU", True, self.cores['branco'])

            pygame.draw.rect(self.tela, self.cores['azul'], botoes[0], border_radius=14)
            pygame.draw.rect(self.tela, self.cores['azul'], botoes[1], border_radius=14)
            pygame.draw.rect(self.tela, self.cores['branco'], botoes[0], 2, border_radius=14)
            pygame.draw.rect(self.tela, self.cores['branco'], botoes[1], 2, border_radius=14)

            self.tela.blit(texto_reiniciar, texto_reiniciar.get_rect(center=botoes[0].center))
            self.tela.blit(texto_menu, texto_menu.get_rect(center=botoes[1].center))

        pygame.display.update()

    def processar_eventos(self):
        # Lê os eventos do Pygame e atualiza o estado do jogo.
        # Retorna False quando o jogo deve ser finalizado.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado == "menu" and evento.button == 1:
                    for index, botao in enumerate(self._calcular_retangulos_menu()):
                        if botao.collidepoint(evento.pos):
                            self._iniciar_jogo(self.menu_opcoes[index])
                            break
                    continue

                if self.estado == "jogo" and self.fim_jogo and evento.button == 1:
                    botoes = self._calcular_retangulos_game_over()
                    if botoes[0].collidepoint(evento.pos):
                        self._reiniciar_partida()
                    elif botoes[1].collidepoint(evento.pos):
                        self._reset_para_menu()
                    continue

                if self.estado == "jogo" and not self.fim_jogo:
                    x, y = evento.pos
                    j = x // self.tamanho_celula
                    i = (y - self.altura_hud) // self.tamanho_celula

                    if not (0 <= i < self.linhas and 0 <= j < self.colunas):
                        continue

                    if evento.button == 1:  # Botão esquerdo
                        if not self.tabuleiro.grid[i][j].marcada:
                            self.tabuleiro.revelar(i, j)
                            sons.som_click.play()
                            if self.tabuleiro.grid[i][j].tem_mina:
                                sons.som_mina.play()
                                self.fim_jogo = True
                                self.vitoria = False
                                self.tempo_final = pygame.time.get_ticks()
                                self._revelar_todas_minas()
                            elif self.tabuleiro.verificar_vitoria():
                                self.fim_jogo = True
                                self.vitoria = True
                                self.tempo_final = pygame.time.get_ticks()
                                sons.som_vitoria.play()
                    elif evento.button == 3:  # Botão direito
                        self.tabuleiro.alternar_marca(i, j)
                        sons.som_flag.play()

            if evento.type == pygame.KEYDOWN:
                if self.estado == "menu":
                    if evento.key == pygame.K_1:
                        self._iniciar_jogo(self.menu_opcoes[0])
                    elif evento.key == pygame.K_2:
                        self._iniciar_jogo(self.menu_opcoes[1])
                    elif evento.key == pygame.K_3:
                        self._iniciar_jogo(self.menu_opcoes[2])

                if evento.key == pygame.K_r:
                    self.tabuleiro = Tabuleiro(
                        self.linhas,
                        self.colunas,
                        self.minas)
                    self._ajustar_assets(self.tamanho_celula)
                    self._redefinir_tela()
                    self.fim_jogo = False
                    self.vitoria = False
                    self.tempo_inicial = pygame.time.get_ticks()

                if evento.key == pygame.K_ESCAPE:
                    self._reset_para_menu()

                if self.estado == "jogo" and self.fim_jogo and evento.key == pygame.K_m:
                    self._reset_para_menu()

                if evento.key == pygame.K_q:
                    return False

        return True

    def _reiniciar_partida(self):
        # Reinicia a partida atual mantendo a dificuldade escolhida.
        self.tabuleiro = Tabuleiro(
            self.linhas,
            self.colunas,
            self.minas)
        self._ajustar_assets(self.tamanho_celula)
        self._redefinir_tela()
        self.fim_jogo = False
        self.vitoria = False
        self.tempo_inicial = pygame.time.get_ticks()

    def _reset_para_menu(self):
        # Retorna ao menu principal e zera o estado do jogo.
        self.estado = "menu"
        self.linhas = 9
        self.colunas = 9
        self.minas = 10
        self.tamanho_celula = self.menu_tamanho_celula
        self._ajustar_assets(self.tamanho_celula)
        self.largura = self.menu_largura
        self.altura = self.menu_altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        self.fim_jogo = False
        self.vitoria = False
        self.tempo_final = None
        self.tempo_inicial = pygame.time.get_ticks()

    def _calcular_retangulos_menu(self):
        # Retorna os retângulos dos botões do menu principal.
        largura_botao = min(560, self.largura - 160)
        altura_botao = 90
        espacamento = 24
        x = (self.largura - largura_botao) // 2
        y_inicial = 200
        return [pygame.Rect(x, y_inicial + index * (altura_botao + espacamento), largura_botao, altura_botao)
                for index in range(len(self.menu_opcoes))]

    def _calcular_retangulos_game_over(self):
        # Calcula a posição dos botões do game over, sempre abaixo do texto de tempo final.
        largura_botao = 160
        altura_botao = 50
        espacamento = 20
        x = self.largura // 2 - largura_botao - espacamento // 2
        y = self.altura // 2 + 80
        botao_reiniciar = pygame.Rect(x, y, largura_botao, altura_botao)
        botao_menu = pygame.Rect(x + largura_botao + espacamento, y, largura_botao, altura_botao)
        return [botao_reiniciar, botao_menu]

    def _ajustar_assets(self, tamanho_celula):
        # Ajusta o tamanho dos ícones do jogo conforme as células do tabuleiro.
        escala = 30 if tamanho_celula >= 30 else max(18, tamanho_celula - 5)
        self.mina_img = pygame.transform.smoothscale(self.mina_img_original, (escala, escala))
        self.mina_hud_img = pygame.transform.smoothscale(self.mina_img_original, (escala, escala))
        self.bandeira_img = pygame.transform.smoothscale(self.bandeira_img_original, (escala, escala))
        self.relogio_img = pygame.transform.smoothscale(self.relogio_img_original, (30, 30))

    def _redefinir_tela(self):
        # Recalcula a janela sempre que a dificuldade ou o tamanho do tabuleiro muda.
        self.largura = self.colunas * self.tamanho_celula
        self.altura = self.linhas * self.tamanho_celula + self.altura_hud
        self.tela = pygame.display.set_mode((self.largura, self.altura))

    def _iniciar_jogo(self, opcao):
        # Inicia uma nova partida com a dificuldade selecionada no menu.
        self.estado = "jogo"
        self.linhas = opcao['linhas']
        self.colunas = opcao['colunas']
        self.minas = opcao['minas']
        self.tamanho_celula = opcao.get('tamanho_celula', 40)
        self.tabuleiro = Tabuleiro(self.linhas, self.colunas, self.minas)
        self._ajustar_assets(self.tamanho_celula)
        self._redefinir_tela()
        self.fim_jogo = False
        self.vitoria = False
        self.tempo_inicial = pygame.time.get_ticks()

        return True

    def _revelar_todas_minas(self):
        # Revela todas as minas no tabuleiro após derrota.
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.tabuleiro.grid[i][j].tem_mina:
                    self.tabuleiro.grid[i][j].revelada = True

    def executar(self):
        # Loop principal do jogo: processa eventos, desenha a cena e controla o FPS.
        rodando = True
        relogio = pygame.time.Clock()
        
        while rodando:
            rodando = self.processar_eventos()
            self.desenhar()
            relogio.tick(30)
            
        pygame.quit()