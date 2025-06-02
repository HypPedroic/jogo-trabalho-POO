import pygame
from .entidade import Entidade

class Player(Entidade):
    def __init__(self, game, pos, tamanho):
        super().__init__(game, 'player', pos, tamanho)
        self._vida = 100
        self._furia = 0
        self._puloDuplo = True
        self._iFrames = False
        self._air_time = 0

    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        self._vida = valor

    @property
    def furia(self):
        return self._furia
    
    @furia.setter
    def furia(self, valor):
        self._furia = valor

    @property
    def puloDuplo(self):
        return self._puloDuplo
    
    @puloDuplo.setter
    def puloDuplo(self, valor):
        self._puloDuplo = valor

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
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(movement)

        self.air_time += 1
        if self.colisoes['baixo']:
            self.air_time = 0
        
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')



