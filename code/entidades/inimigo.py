# Importando as bibliotecas necessárias
import pygame
import math
import random
from entidades.fisica_entidade import FisicaEntidade

# Classe base para inimigos
class Inimigo(FisicaEntidade):
    def __init__(self, game, tipo, pos, tamanho, vida=3):
        super().__init__(game, tipo, pos, tamanho)
        self._vida = vida
        self._vida_maxima = vida
        self._direcao = 1  # 1 para direita, -1 para esquerda
        self._tempo_ataque = 0
        self._intervalo_ataque = 120  # 2 segundos entre ataques
        self._ativo = True
        self._dano = 1
        self._velocidade_movimento = 1
        self._alcance_deteccao = 200
        self._animacao_frame = 0
        self._animacao_velocidade = 0.1
        self._estado = 'parado'  # 'parado', 'correndo', 'atacando'
        self._distancia_deteccao = 150  # distância para detectar o jogador
        
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, value):
        self._vida = value
        if self._vida <= 0:
            self._ativo = False
    
    @property
    def ativo(self):
        return self._ativo
    
    @ativo.setter
    def ativo(self, value):
        self._ativo = value
    
    @property
    def dano(self):
        return self._dano
    
    @dano.setter
    def dano(self, value):
        self._dano = value
    
    def receber_dano(self, dano):
        """Método para o inimigo receber dano"""
        self._vida -= dano
        if self._vida <= 0:
            self._ativo = False
    
    def detectar_jogador(self):
        """Verifica se o jogador está próximo o suficiente para ser detectado"""
        if not self._ativo:
            return False
            
        jogador_pos = self.game.player.pos
        dx = jogador_pos[0] - self.pos[0]
        dy = jogador_pos[1] - self.pos[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia <= self._distancia_deteccao:
            # Atualiza a direção baseada na posição do jogador
            self._direcao = 1 if dx > 0 else -1
            return True
        return False
    
    def colidir_com_jogador(self):
        """Verifica se o inimigo está colidindo com o jogador"""
        if not self._ativo:
            return False
            
        return self.retangulo().colliderect(self.game.player.retangulo())
    
    def update(self, movement=(0, 0)):
        """Atualiza o estado do inimigo"""
        if not self._ativo:
            return
            
        # Incrementa o tempo desde o último ataque
        self._tempo_ataque += 1
        
        # Comportamento básico: movimento de patrulha
        if not self.detectar_jogador():
            # Inverte direção se colidir com parede
            if self.colisoes['esquerda'] or self.colisoes['direita']:
                self._direcao *= -1
            
            movement = (self._velocidade_movimento * self._direcao, 0)
        
        # Chama o método update da classe pai
        super().update(movement)
        
        # Verifica colisão com o jogador
        if self.colidir_com_jogador():
            self.game.player.receber_dano(self._dano)
    
    def renderizar(self, surf, offset=(0, 0)):
        """Renderiza o inimigo na tela"""
        if not self._ativo:
            return
            
        # Renderiza o inimigo
        surf.blit(self.game.assets[self.e_tipo], (self.pos[0] - offset[0], self.pos[1] - offset[1]))