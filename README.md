# ReaperQuest 💀

ReaperQuest é um jogo de ação em plataforma feito com Python e Pygame, onde você controla um ceifador enfrentando hordas de inimigos em mapas desafiadores. O objetivo é sobreviver, derrotar todos os inimigos e alcançar a vitória!

## Como jogar

- **Inicie o jogo** executando `python code/jogo.py`.
- No menu principal, escolha:
  - **JOGAR**: Inicia uma nova partida (você pode digitar seu nome e escolher a dificuldade).
  - **CONTINUAR PARTIDA**: (Aparece se houver progresso salvo) Retoma do ponto exato onde você salvou.
  - **RANKING**: Veja os melhores tempos.
  - **SAIR**: Fecha o jogo.

## Mecânicas principais

- **Movimentação**: Ande, pule e ataque inimigos em um mapa 2D.
- **Fúria**: Ao derrotar inimigos, encha a barra de fúria e ative o modo especial com a tecla `Q`.
- **Salvar progresso**: Pause o jogo com `ESC` ou `P` e salve seu progresso para continuar depois.
- **Game Over/Vitória**: Se perder ou vencer, o progresso salvo é apagado automaticamente.

## Controles do jogo

| Tecla           | Função                               |
| --------------- | ------------------------------------ |
| ←, →            | Mover para esquerda/direita          |
| ↑               | Pular                                |
| Espaço          | Atacar                               |
| Q               | Ativar modo fúria (quando cheio)     |
| ESC             | Pausar o jogo / abrir menu de pausa  |
| P               | Pausar/despausar a música            |
| + / -           | Aumentar / diminuir volume da música |
| ENTER           | Confirmar seleção/menu               |
| Seta cima/baixo | Navegar entre botões do menu         |

## Menu de pausa

- **Salvar**: Salva o progresso atual (posição, vida, inimigos, tempo, etc).
- **Sair**: Fecha o jogo imediatamente.
- **Voltar**: Retorna ao jogo.

## Sistema de progresso

- O progresso é salvo em `data/save.json`.
- Só é possível continuar se houver um progresso salvo.
- O progresso é removido automaticamente ao vencer ou perder a partida.

## Ranking

- O ranking mostra os melhores tempos dos jogadores.
- O ranking é salvo em `data/ranking.json`.

## Requisitos

- Python 3.8+
- Pygame 2.x

## Instalação

1. Instale as dependências:
   ```bash
   pip install pygame
   ```
2. Execute o jogo:
   ```bash
   python code/jogo.py
   ```

Desenvolvido para disciplina de Programação Orientada a Objetos.

Sobre o editor de mapas:

W, A, S, D movem a câmera
Click do mouse coloca o objeto
Click direito remove o objeto
G muda o modo de edição para offgrid, para colocar decorações
K salva o mapa, se for criar um mapa novo, lembre de mudar o path
SHIFT + scroll do mouse muda a variante do objeto
scroll muda o tipo de objeto

