import pygame
import time

from code.entidades.entidade import Entidade
from utils.utils import load_images
from utils.animation import Animation

class Esqueleto(Entidade):
    def __init__(self, game, x, y, tamanho=(16, 32)):
        # Carrega as animações do esqueleto
        assets = {
            'idle': Animation(load_images('inimigos/esqueleto/idle'), img_dur=6, loop=True),
            'andar': Animation(load_images('inimigos/esqueleto/andar'), img_dur=6, loop=True),
            'ataque': Animation(load_images('inimigos/esqueleto/ataque'), img_dur=4, loop=False),
            'morrer': Animation(load_images('inimigos/esqueleto/morrer'), img_dur=6, loop=False),
        }
        super().__init__(assets, (x, y), tamanho)
        self.game = game
        self.vida = 3
        self.atacando = False
        self.morto = False
        self.dano = 1
        self.velocidade_inimigo = 1
        self.cooldown_tiro = 2.0  # segundos
        self.ultimo_tiro = time.time()

    def update(self, tilemap, player):
        if self.morto:
            self.set_action('morrer')
        elif self.atacando:
            self.set_action('ataque')
        else:
            # Movimento simples em direção ao player
            if player.pos[0] < self.pos[0]:
                self.mover_esquerda(True)
                self.mover_direita(False)
                self.set_action('andar')
            elif player.pos[0] > self.pos[0]:
                self.mover_direita(True)
                self.mover_esquerda(False)
                self.set_action('andar')
            else:
                self.mover_direita(False)
                self.mover_esquerda(False)
                self.set_action('idle')

            # Lógica para atirar ossos
            self.tentar_atirar(player)
        super().update(tilemap)

    def tentar_atirar(self, player):
        agora = time.time()
        if agora - self.ultimo_tiro >= self.cooldown_tiro:
            self.atirar_ossos(player)
            self.ultimo_tiro = agora

    def atirar_ossos(self, player):
        # Importa a classe Projetil
        from code.projeteis.projeteis import Projetil
        # Define a direção do tiro (direita ou esquerda)
        direcao = [False, False]
        if player.pos[0] < self.pos[0]:
            direcao = [False, True]  # Esquerda
        else:
            direcao = [True, False]  # Direita
        # Cria o projétil (você pode trocar o tamanho e offset depois)
        osso = Projetil(
            pos=[self.pos[0], self.pos[1]],
            tamanho=(16, 16),
            movimento=direcao
        )
        # Adiciona o projétil na lista de projéteis do jogo
        if hasattr(self.game, 'lista_projeteis'):
            self.game.lista_projeteis.append(osso)
        else:
            print('AVISO: game não possui lista_projeteis!')

    def atacar(self, player):
        if not self.morto and not self.atacando:
            self.atacando = True
            # Aqui você pode adicionar lógica para causar dano ao player
            player.vida -= self.dano

    def morrer(self):
        self.morto = True

    def renderizar(self, surf, offset=(0, 0)):
        super().renderizar(surf, offset)