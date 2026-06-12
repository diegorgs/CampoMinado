# Campo Minado

Projeto desenvolvido em Python utilizando a biblioteca Pygame como trabalho acadêmico.

## Sobre o Projeto

O Campo Minado é um jogo de lógica em que o objetivo é revelar todas as células que não possuem minas. O jogador utiliza pistas numéricas para identificar a localização das minas e marcá-las com bandeiras.

O projeto foi desenvolvido com foco na aplicação de conceitos de programação orientada a objetos, manipulação de eventos, interface gráfica e organização de código em módulos.

## Tecnologias Utilizadas

- Python 3
- Pygame

## Estrutura do Projeto

```
CampoMinado/
│
├── assets/
│   ├── mina.png
│   ├── flags.png
│   ├── relogio.png
│   └── sons/
│
├── core/
│   ├── celula.py
│   ├── tabuleiro.py
│   └── sons.py
│
├── gui/
│   └── jogo_pygame.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Funcionalidades

- Menu inicial com seleção de dificuldade.
- Três níveis de dificuldade:
  - Iniciante (9x9)
  - Difícil (16x16)
  - Impossível (24x24)
- Contador de tempo.
- Contador de minas restantes.
- Sistema de bandeiras.
- Efeitos sonoros.
- Tela de vitória.
- Tela de derrota.
- Reinício rápido da partida.
- Retorno ao menu principal.

## Como Executar

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o jogo

```bash
python main.py
```

## Controles

| Ação | Tecla |
|--------|--------|
| Revelar célula | Clique esquerdo |
| Colocar bandeira | Clique direito |
| Reiniciar partida | R |
| Voltar ao menu | ESC |
| Sair do jogo | Q |

## Conceitos Aplicados

- Programação Orientada a Objetos
- Recursividade
- Manipulação de Matrizes
- Tratamento de Eventos
- Interface Gráfica com Pygame
- Modularização de Código

## Autor

Carlos Eduardo
Diego Rodrigues
Matheus Cleto

Projeto desenvolvido para fins acadêmicos.




## Desafios Encontrados

- Implementação do primeiro clique seguro.
- Redimensionamento automático para diferentes resoluções.
- Centralização de elementos da interface.
- Ajuste dos ícones e fontes para diferentes dificuldades.
- Geração do executável (.exe) utilizando PyInstaller.