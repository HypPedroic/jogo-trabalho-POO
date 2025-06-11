import pygame
from .entidade import Entidade
from utils.utils import load_images
from utils.animation import Animation
from projeteis.projeteis import Projetil

class Player(Entidade):
    def __init__(self, pos, tamanho):
        # Carregando os assets do player
        self.assets = {
            'idle': Animation(load_images('player/idle'), img_dur=12),
            'run': Animation(load_images('player/run'), img_dur=24),
            'jump': Animation(load_images('player/jump'), img_dur=16),
            'idleFoice': Animation(load_images('player/idleFoice'), img_dur=12),
            'runFoice': Animation(load_images('player/runFoice'), img_dur=24),
            'jumpFoice': Animation(load_images('player/jumpFoice'), img_dur=16),
            'attack': Animation(load_images('player/attack'), img_dur=8),
        }
        
        # Chamando o construtor da classe pai
        super().__init__(self.assets, pos, tamanho)
        
        self._vidaMax = 3
        self._vida = self._vidaMax
        self._estado = 'normal'
        self._furia = 5
        self._pulos_disponiveis = 2
        self._iFrames = False
        self._air_time = 0
        self._atacando = 0

    @property
    def vidaMax(self):
        return self._vidaMax
    
    @vidaMax.setter
    def vidaMax(self, valor):
        self._vidaMax = valor

    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        self._vida = valor

    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, valor):
        self._estado = valor

    @property
    def pulos_disponiveis(self):
        return self._pulos_disponiveis
    
    @pulos_disponiveis.setter
    def pulos_disponiveis(self, valor):
        self._pulos_disponiveis = valor

    @property
    def iFrames(self):
        return self._iFrames
    
    @property
    def air_time(self):
        return self._air_time
    
    @air_time.setter
    def air_time(self, valor):
        self._air_time = valor
    
    @iFrames.setter
    def iFrames(self, valor):
        self._iFrames = valor

    @property
    def tempo_queda(self):
        return self._tempo_queda
    
    @tempo_queda.setter
    def tempo_queda(self, valor):
        self._tempo_queda = valor

    @property
    def tempo_max_queda(self):
        return self._tempo_max_queda
    
    @tempo_max_queda.setter
    def tempo_max_queda(self, valor):
        self._tempo_max_queda = valor

    @property
    def caindo(self):
        return self._caindo
    
    @caindo.setter
    def caindo(self, valor):
        self._caindo = valor
    
    @property
    def furia(self):
        return self._furia
    
    @furia.setter
    def furia(self, valor):
        self._furia = valor

    @property
    def atacando(self):
        return self._atacando
    
    @atacando.setter
    def atacando(self, valor):
        self._atacando = valor
    
    def update(self, tilemap, game):
        super().update(tilemap)
        self.animacao_atual(game)

    def fisica_colisao_Y(self, tilemap):
        super().fisica_colisao_Y(tilemap)
        self.air_time += 1
        if self.colisoes['baixo']:
            self.air_time = 0
            self.pulos_disponiveis = 2

    def pular(self):
        if self.pulos_disponiveis > 1:
            self.velocidade[1] = -6
            self.pulos_disponiveis -= 1
            self.air_time = 5
        elif self.pulos_disponiveis == 1:
            self.velocidade[1] = -6
            self.pulos_disponiveis -= 1
            self.air_time = 5

    def ativar_furia(self):
        if self.furia == 100:
            self.estado = 'foice'

    def atacar(self):
        if self.estado == 'normal':
            self.atacando = 64
        elif self.estado == 'foice':
            pass

    def ataque_normal(self, game):
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

    def ataque_furia(self):
        pass

    def animacao_atual(self, game):
        if self.atacando > 0:
            self.set_action('attack')
            self.atacando -= 1
            if self.atacando == 24:
                self.ataque_normal(game)
        elif self.air_time > 4:
            if self.estado == 'normal':
                self.set_action('jump')
            elif self.estado == 'foice':
                self.set_action('jumpFoice')
        elif self.movimento[0] or self.movimento[1]:  # Se está se movendo para qualquer direção
            if self.estado == 'normal':
                self.set_action('run')
            elif self.estado == 'foice':
                self.set_action('runFoice')
        else:
            if self.estado == 'normal':
                self.set_action('idle')
            elif self.estado == 'foice':
                self.set_action('idleFoice')
                

