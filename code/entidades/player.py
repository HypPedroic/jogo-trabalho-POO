import pygame
from .entidade import Entidade
from utils.utils import load_images
from utils.animation import Animation

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
        }
        
        # Chamando o construtor da classe pai
        super().__init__(self.assets, pos, tamanho)
        
        self._vidaMax = 3
        self._vida = self._vidaMax
        self._estado = 'normal'
        self._pulos_disponiveis = 2
        self._iFrames = False
        self._air_time = 0
        self._tempo_queda = 0  # Tempo desde que começou a cair
        self._tempo_max_queda = 15  # Tempo máximo antes de perder os pulos (ajuste conforme necessário)
        self._caindo = False  # Flag para identificar se está caindo sem ter pulado

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
    
    def update(self, tilemap):
        super().update(tilemap)



        self.air_time += 1
        
        # Verifica se está no chão
        if self.colisoes['baixo']:
            self.air_time = 0
            self.pulos_disponiveis = 2
            self._tempo_queda = 0
            self._caindo = False
        else:
            # Se não está no chão e não está subindo (velocidade positiva = caindo)
            if self.velocidade[1] > 0 and not self._caindo:
                self._caindo = True
                self._tempo_queda = 0
            
            # Se está caindo, incrementa o tempo de queda
            if self._caindo:
                self._tempo_queda += 1
                # Se passou do tempo máximo e ainda tem pulos disponíveis
                if self._tempo_queda >= self._tempo_max_queda and self.pulos_disponiveis > 1:
                    self.pulos_disponiveis = 1
        
        if self.air_time > 4:
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

    def pular(self):
        if self.pulos_disponiveis > 1:
            self.velocidade[1] = -6
            self.pulos_disponiveis -= 1
            self.air_time = 5
            self._caindo = False  # Reseta o estado de queda ao pular
        elif self.pulos_disponiveis == 1:
            self.velocidade[1] = -6
            self.pulos_disponiveis -= 1
            self.air_time = 5
            self._caindo = False  # Reseta o estado de queda ao pular

    def alterar_estado(self):
        if self.estado == 'normal':
            self.estado = 'foice'
            self.anim_offeset = (-8, -16)
        elif self.estado == 'foice':
            self.estado = 'normal'
            self.anim_offeset = (-8, 0)

