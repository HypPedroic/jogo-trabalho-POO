import pygame
import math
import random
from entidades.entidade import Entidade
from utils.utils import load_images
from utils.animation import Animation
from projeteis.projeteis import Projetil
from particles.particles import Particle

class Player(Entidade):
    def __init__(self, pos, tamanho):
        # Carregando os assets do player
        self.__assets = {
            'idle': Animation(load_images('player/idle'), img_dur=12),
            'run': Animation(load_images('player/run'), img_dur=24),
            'jump': Animation(load_images('player/jump'), img_dur=16),
            'idleFoice': Animation(load_images('player/idleFoice'), img_dur=12),
            'runFoice': Animation(load_images('player/runFoice'), img_dur=24),
            'jumpFoice': Animation(load_images('player/jumpFoice'), img_dur=16),
            'attack': Animation(load_images('player/attack'), img_dur=8, loop=False),
        }
        
        # Chamando o construtor da classe pai
        super().__init__(self.__assets, pos, tamanho)
        
        self.anim_offeset = [-8, 0]
        self.__vidaMax = 3
        self.__vida = self.__vidaMax
        self.__estado = 'normal'
        self.__furia = 0
        self.__pulos_disponiveis = 2
        self.__iframe_timer = 0
        self.__air_time = 0
        self.__atacando = 0
        self.__dashing = 0

    @property
    def vidaMax(self):
        return self.__vidaMax
    
    @vidaMax.setter
    def vidaMax(self, valor):
        self.__vidaMax = valor

    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, valor):
        self.__vida = valor

    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    @property
    def pulos_disponiveis(self):
        return self.__pulos_disponiveis
    
    @pulos_disponiveis.setter
    def pulos_disponiveis(self, valor):
        self.__pulos_disponiveis = valor
    
    @property
    def air_time(self):
        return self.__air_time
    
    @air_time.setter
    def air_time(self, valor):
        self.__air_time = valor
    
    @property
    def furia(self):
        return self.__furia
    
    @furia.setter
    def furia(self, valor):
        self.__furia = valor

    @property
    def atacando(self):
        return self.__atacando
    
    @atacando.setter
    def atacando(self, valor):
        self.__atacando = valor
        
    @property
    def iframe_timer(self):
        return self.__iframe_timer
    
    @iframe_timer.setter
    def iframe_timer(self, valor):
        self.__iframe_timer = valor
        
    @property
    def dashing(self):
        return self.__dashing
    
    @dashing.setter
    def dashing(self, valor):
        self.__dashing = valor
    
    def update(self, tilemap, game):
        super().update(tilemap)
        
        self.verificar_limbo(tilemap)
        
        if self.atacando > 0:
            self.__atacando -= 1
            if self.__atacando == 56:
                self.__ataque_normal(game)
            if self.__atacando <= 0:
                self.atacando = 0
        
        if self.estado == 'foice':
            self.furia -= 0.1
            if self.furia <= 0:
                self.furia = 0
                self.estado = 'normal'
                self.anim_offeset = [-8, 0]
        
        # Atualiza iframes
        if self.iframe_timer > 0:
            self.__iframe_timer -= 1
            
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocidade = [math.cos(angle)*speed, math.sin(angle)*speed]
                game.particulas.append(Particle('dash', self.retangulo().center, pvelocidade, frame=random.randint(0, 7)))          
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocidade[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocidade[0] *= 0.1
            pvelocidade = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            game.particulas.append(Particle('dash', self.retangulo().center, pvelocidade, frame=random.randint(0, 7)))       
        if self.velocidade[0] > 0:
            self.velocidade[0] = max(self.velocidade[0] - 0.1, 0)
        else:
            self.velocidade[0] = min(self.velocidade[0] + 0.1, 0)
                 
                
        self.__animacao_atual(game)

    def fisica_colisao_Y(self, tilemap):
        super().fisica_colisao_Y(tilemap)
        self.__air_time += 1
        if self.colisoes['baixo']:
            self.__air_time = 0
            self.__pulos_disponiveis = 2

    def pular(self):
        if self.__pulos_disponiveis > 1:
            self.velocidade[1] = -6
            self.__pulos_disponiveis -= 1
            self.__air_time = 5
        elif self.__pulos_disponiveis == 1:
            self.velocidade[1] = -6
            self.__pulos_disponiveis -= 1
            self.__air_time = 5

    def ativar_furia(self, game=None):
        if self.furia == 100:
            self.estado = 'foice'
            # Toca som de fúria
            self.anim_offeset = [-8, -16]
            self.vida = self.vidaMax
            if game:
                game.tocar_som('furia')

    def atacar(self):
        if self.estado == 'normal':
            if not self.atacando:
                self.atacando = 96
        elif self.estado == 'foice':
            if not self.dashing:
                if self.flip:
                    self.dashing = -60
                else:
                    self.dashing = 60

    def __ataque_normal(self, game):
        if self.flip:
            x = self.pos[0] - self.tamanho[0]
        else:
            x = self.pos[0] + self.tamanho[0]
            
        y = self.pos[1]
            
        if self.flip == True:
            direcao = [False, True]
        else:
            direcao = [True, False]

        projetil = Projetil([x, y], [32, 32], direcao)
        
        game.projeteis.append(projetil)
        
        # Toca som de tiro
        game.tocar_som('tiro')
        
    def receber_dano(self, dano=1, game=None):
        """Player recebe dano de inimigos"""
        if self.iframe_timer == 0 and abs(self.dashing) <= 40:  # Só recebe dano se não estiver em iframes
            self.vida -= dano
            # iFrames duram 60 frames (1 segundo a 60fps)
            self.iframe_timer = 60
            
            # Toca som de dano
            if game:
                game.tocar_som('dano')
            
            if self.vida <= 0:
                self.vida = 0
                # Player morreu
                return True
        return False

    def __animacao_atual(self, game):
        if self.__atacando > 0:
            if self.__atacando > 32:
                self.set_action('attack')
        elif self.__air_time > 4:
            if self.__estado == 'normal':
                self.set_action('jump')
            elif self.__estado == 'foice':
                self.set_action('jumpFoice')
        elif self.movimento[0] or self.movimento[1]:  # Se está se movendo para qualquer direção
            if self.__estado == 'normal':
                self.set_action('run')
            elif self.__estado == 'foice':
                self.set_action('runFoice')
        else:
            if self.__estado == 'normal':
                self.set_action('idle')
            elif self.__estado == 'foice':
                self.set_action('idleFoice')
                
    def verificar_limbo(self, tilemap):
        if self and self.retangulo().y > tilemap.limite_mapa_y:
            self.vida = 0
            
    def renderizar(self, surf, offset=(0, 0)):
        if self.iframe_timer > 0 and (self.iframe_timer // 3) % 2 == 0:
            return  # Não desenha neste frame (efeito de piscar)
        if abs(self.dashing) <= 50:
            super().renderizar(surf, offset)
        
        

            