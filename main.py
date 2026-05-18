from gui.jogo_pygame import JogoCampoMinado

def main():
    """Ponto de entrada principal do jogo Campo Minado."""
    jogo = JogoCampoMinado(linhas=9, colunas=9, minas=10, tamanho_celula=40)
    jogo.executar()

if __name__ == "__main__":
    main()