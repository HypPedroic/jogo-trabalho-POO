import pygame
from entidades.entidade import Entidade
from utils.utils import load_images
from utils.animation import Animation
from projeteis.projeteis import Projetil

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
            'attack': Animation(load_images('player/attack'), img_dur=8),
        }
        
        # Chamando o construtor da classe pai
        super().__init__(self.__assets, pos, tamanho)
        
        self.__vidaMax = 3
        self.__vida = self.__vidaMax
        self.__estado = 'normal'
        self.__furia = 5
        self.__pulos_disponiveis = 2
        self.__iFrames = False
        self.__iframe_timer = 0
        self.__air_time = 0
        self.__atacando = 0
        self.__tempo_queda = 0
        self.__tempo_max_queda = 0
        self.__caindo = False

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
    def iFrames(self):
        return self.__iFrames
    
    @property
    def air_time(self):
        return self.__air_time
    
    @air_time.setter
    def air_time(self, valor):
        self.__air_time = valor
    
    @iFrames.setter
    def iFrames(self, valor):
        self.__iFrames = valor

    @property
    def tempo_queda(self):
        return self.__tempo_queda
    
    @tempo_queda.setter
    def tempo_queda(self, valor):
        self.__tempo_queda = valor

    @property
    def tempo_max_queda(self):
        return self.__tempo_max_queda
    
    @tempo_max_queda.setter
    def tempo_max_queda(self, valor):
        self.__tempo_max_queda = valor

    @property
    def caindo(self):
        return self.__caindo
    
    @caindo.setter
    def caindo(self, valor):
        self.__caindo = valor
    
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
    
    def update(self, tilemap, game):
        super().update(tilemap)
        
        # Atualiza iframes
        if self.__iFrames and self.__iframe_timer > 0:
            self.__iframe_timer -= 1
            if self.__iframe_timer <= 0:
                self.__iFrames = False
                
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
        if self.__furia == 100:
            self.__estado = 'foice'
            # Toca som de fúria
            if game:
                game.tocar_som('furia')

    def atacar(self):
        if self.__estado == 'normal':
            self.__atacando = 64
        elif self.__estado == 'foice':
            pass

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

    def __ataque_furia(self):
        pass
        
    def receber_dano(self, dano=1, game=None):
        """Player recebe dano de inimigos"""
        if not self.__iFrames:  # Só recebe dano se não estiver em iframes
            self.__vida -= dano
            self.__iFrames = True
            # iFrames duram 60 frames (1 segundo a 60fps)
            self.__iframe_timer = 60
            
            # Toca som de dano
            if game:
                game.tocar_som('dano')
            
            if self.__vida <= 0:
                self.__vida = 0
                # Player morreu
                return True
        return False

    def __animacao_atual(self, game):
        if self.__atacando > 0:
            self.set_action('attack')
            self.__atacando -= 1
            if self.__atacando == 24:
                self.__ataque_normal(game)
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
                

