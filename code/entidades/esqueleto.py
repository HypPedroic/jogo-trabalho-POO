import pygame
import random
import math
from .entidade import Entidade
from utils.utils import load_images
from animation.animation import Animation
from projeteis.projeteis import Projetil

class Esqueleto(Entidade):
    def __init__(self, pos, tamanho, game):
        
        self.__assets = {
            'idle': Animation(load_images('isqueleto/idle'), img_dur=8),
            'inativo': Animation(load_images('isqueleto/inativo'), img_dur=1),
            'acordar': Animation(load_images('isqueleto/acordar'), img_dur=14, loop=False),
            'dormir': Animation(load_images('isqueleto/dormir'), img_dur=14, loop=False),
            'atacar': Animation(load_images('isqueleto/atacar'), img_dur=6, loop=False),
            'morrer': Animation(load_images('isqueleto/morrer'), img_dur=4, loop=False),
        }
        
        super().__init__(self.__assets, pos, tamanho)
        
        self.__game = None
        self.__vida = 2
        self.__vida_maxima = 2
        self.__estado = 'inativo' # inativo, acordando, ativo, atacando, dormindo, morto
        self.__animDur = 0
        self.__alcance_deteccao = 250
        self.__iframes = 0
        self.__cont = 0
        self.__player = None
        self.__game = game
        self.__espera_ataque = 0
        self.__ja_viu_player = False  # Flag para não voltar a dormir após ver o player
        
    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, valor):
        self.__vida = valor
        
    @property
    def vida_maxima(self):
        return self.__vida_maxima

    @vida_maxima.setter
    def vida_maxima(self, valor):
        self.__vida_maxima = valor
        
    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, valor):
        self.__estado = valor
        
    @property
    def iFrames(self):
        return self.__iFrames

    @iFrames.setter
    def iFrames(self, valor):
        self.__iFrames = valor
        
    @property
    def alcance_deteccao(self):
        return self.__alcance_deteccao
    
    @alcance_deteccao.setter
    def alcance_deteccao(self, valor):
        self.__alcance_deteccao = valor
        
    @property
    def animDur(self):
        return self.__animDur
    
    @animDur.setter
    def animDur(self, valor):
        self.__animDur = valor

    @property
    def iframes(self):
        return self.__iframes

    @iframes.setter
    def iframes(self, valor):
        self.__iframes = valor
        
    @property
    def cont(self):
        return self.__cont
    
    @cont.setter
    def cont(self, valor):
        self.__cont = valor
        
    @property
    def player(self):
        return self.__player
    
    @player.setter
    def player(self, valor):
        self.__player = valor
        
    @property
    def game(self):
        return self.__game
    
    @game.setter
    def game(self, valor):
        self.__game = valor
        
    @property
    def espera_ataque(self):
        return self.__espera_ataque
    
    @espera_ataque.setter
    def espera_ataque(self, valor):
        self.__espera_ataque = valor
        
    @property
    def ja_viu_player(self):
        return self.__ja_viu_player
    
    @ja_viu_player.setter
    def ja_viu_player(self, valor):
        self.__ja_viu_player = valor

    def criar_projetil(self):
        if self.flip:
            x = self.pos[0] - self.tamanho[0]
        else:
            x = self.pos[0] + self.tamanho[0]
            
        y = self.pos[1]
            
        if self.flip == True:
            direcao = [False, True]
        else:
            direcao = [True, False]

        projetil = Projetil([x, y], [16, 16], direcao, tipo='osso')

        self.game.projeteis.append(projetil)

        # Toca som de tiro
        self.game.tocar_som('tiro')

    def receber_dano(self, dano):
        # Permite receber dano mesmo quando inativo (dormindo) se for atacado pelo player
        if self.iframes <= 0 and self.estado != 'morto':
            self.vida -= dano
            self.iframes = 60
            
            # Se estava inativo e recebeu dano, acorda imediatamente
            if self.estado == 'inativo':
                self.estado = 'acordando'
                self.animDur = 28
                self.cont = 60
            
            # Verifica se morreu
            if self.vida <= 0:
                self.estado = 'morto'
                self.animDur = 8
                
            return True
        return False
    
    def __detectar_jogador(self):
        """Verifica se o jogador está no alcance de detecção"""
        if not self.player or self.__estado == 'morto':
            return False
        
        distancia = math.sqrt(
            (self.player.pos[0] - self.pos[0]) ** 2 + 
            (self.player.pos[1] - self.pos[1]) ** 2
        )
        
        return distancia <= self.__alcance_deteccao
    
    def atacar_jogador(self, game=None):
        """Ataca o jogador se estiver no alcance"""
        if self.pode_atacar_jogador_colisao():
            print("ATACAR")
            self.__estado = 'atacando'
            self.animDur = 14
            
            # Toca som de ataque
            if game:
                game.tocar_som('ataque')
            
            # Aplica dano ao jogador
            if hasattr(self.__player, 'receber_dano'):
                if game:
                    self.player.receber_dano(1, game)
                else:
                    self.player.receber_dano(1)
    
    def pode_atacar_jogador_colisao(self):
        """Verifica se o esqueleto pode atacar o jogador"""
        # Permite ataque mesmo quando inativo (dormindo) se o player estiver no modo fúria
        if self.__player and self.__player.estado == 'foice':
            return self.__estado != 'morto' and self.__iframes == 0
        else:
            return self.__estado != 'morto' and self.__iframes == 0 and self.estado != 'inativo'
    
    
    def direcao_jogador(self):
        if self.estado != 'ativo' or not self.player:
            return
        
        if self.player.pos[0] > self.pos[0]:
            return 'direita'
        elif self.player.pos[0] < self.pos[0]:
            return 'esquerda'
        else:
            return 'mesmo_lugar'
    
    def atacar_com_projetil(self):
        """Ataca o jogador com um projetil"""
        if self.estado == 'ativo' and self.espera_ataque <= 0 and self.pode_atacar_jogador_colisao:
            print("Atacando com projetil")
            self.estado = 'atacando'
            self.animDur = 30
            self.espera_ataque = 120
            
            
            # Toca som de ataque
            self.game.tocar_som('ataque')
        


    def animacao_morte_completa(self):
        return self.estado == 'morto' and self.animDur < 60
    
    def reset(self):
        """Reseta o esqueleto para estado inicial para reuso na pool"""
        self.vida = self.__vida_maxima
        self.estado = self.estado
        self.animDur = 0
        self.iframes = 0
        self.espera_ataque = 0
        self.__ja_viu_player = False

    def update(self, tilemap, player):
        self.player = player
        
        if self.iframes > 0:
            self.iframes -= 1
            if self.iframes <= 0:
                self.iframes = 0
        
        if self.espera_ataque > 0:
            self.espera_ataque -= 1

        if self.direcao_jogador() == 'esquerda':
            self.flip = True
        elif self.direcao_jogador() == 'direita':
            self.flip = False
        
        # Detecta o jogador tanto no modo normal quanto no modo fúria
        if self.__detectar_jogador():
            # Marca que já viu o player
            self.__ja_viu_player = True
            
            if self.estado == 'inativo':
                self.estado = 'acordando'
                self.animDur = 28
                self.cont = 60
            elif self.estado == 'ativo':
                self.cont = 60
                # Só ataca com projétil se o player não estiver no modo fúria
                if self.player.estado != 'foice':
                    self.atacar_com_projetil()
        elif self.estado == 'ativo' and self.cont > 0:
            self.cont -= 1
            # Só volta a dormir se nunca viu o player
            if self.cont <= 0 and not self.__ja_viu_player:
                self.estado = 'dormindo'
                self.animDur = 28

        super().update(tilemap)
        
        self.animacoes()
        
    def animacoes(self):
        if self.estado == 'morto' and self.animDur > 0:
            self.set_action('morrer')
            self.animDur -= 1
        elif self.estado == 'atacando' and self.animDur > 0:
            self.set_action('atacar')
            self.animDur -= 1
            if self.animDur == 10:
                self.criar_projetil()
            if self.animDur <= 0:
                self.estado = 'ativo'
        elif self.estado == 'acordando' and self.animDur > 0:
            self.set_action('acordar')
            self.animDur -= 1
            if self.animDur <= 0:
                self.estado = 'ativo'
        elif self.estado == 'dormindo' and self.animDur > 0:
            self.set_action('dormir')
            self.animDur -= 1
            if self.animDur <= 0:
                self.estado = 'inativo'
        elif self.estado == 'inativo':
            self.set_action('inativo')
        else:
            self.set_action('idle')
    
    def renderizar(self, surf, offset=...):
        if self.iframes > 0 and (self.iframes // 3) % 2 == 0:
            return  # Não desenha neste frame (efeito de piscar)
        super().renderizar(surf, offset)