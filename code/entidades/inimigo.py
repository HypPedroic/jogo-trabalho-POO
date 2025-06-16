# Importando as bibliotecas necessárias
import pygame
import math
import random
from entidades.fisica_entidade import FisicaEntidade

# Classe base para inimigos
class Inimigo(FisicaEntidade):
    def __init__(self, game, tipo, pos, tamanho, vida=3):
        super().__init__(game, tipo, pos, tamanho)
        self.__vida = vida
        self.__vida_maxima = vida
        self.__direcao = 1  # 1 para direita, -1 para esquerda
        self.__tempo_ataque = 0
        self.__intervalo_ataque = 120  # 2 segundos entre ataques
        self.__ativo = True
        self.__dano = 1
        self.__velocidade_movimento = 1
        self.__alcance_deteccao = 200
        self.__animacao_frame = 0
        self.__animacao_velocidade = 0.1
        self.__estado = 'parado'  # 'parado', 'correndo', 'atacando'
        self.__distancia_deteccao = 150  # distância para detectar o jogador
        
    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, value):
        self.__vida = value
        if self.__vida <= 0:
            self.__ativo = False
    
    @property
    def ativo(self):
        return self.__ativo
    
    @ativo.setter
    def ativo(self, value):
        self.__ativo = value
    
    @property
    def dano(self):
        return self.__dano
    
    @dano.setter
    def dano(self, value):
        self.__dano = value
    
    def receber_dano(self, dano):
        """Método para o inimigo receber dano"""
        self.__vida -= dano
        if self.__vida <= 0:
            self.__ativo = False
    
    def __detectar_jogador(self):
        """Verifica se o jogador está próximo o suficiente para ser detectado"""
        if not self.__ativo:
            return False
            
        jogador_pos = self.game.player.pos
        dx = jogador_pos[0] - self.pos[0]
        dy = jogador_pos[1] - self.pos[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia <= self.__distancia_deteccao:
            # Atualiza a direção baseada na posição do jogador
            self.__direcao = 1 if dx > 0 else -1
            return True
        return False
    
    def __colidir_com_jogador(self):
        """Verifica se o inimigo está colidindo com o jogador"""
        if not self.__ativo:
            return False
            
        return self.retangulo().colliderect(self.game.player.retangulo())
    
    def update(self, movement=(0, 0)):
        if not self.__ativo:
            return
            
        # Incrementa o tempo desde o último ataque
        self.__tempo_ataque += 1
        
        # Comportamento básico: movimento de patrulha
        if not self.__detectar_jogador():
            # Inverte direção se colidir com parede
            if self.colisoes['esquerda'] or self.colisoes['direita']:
                self.__direcao *= -1
            
            movement = (self.__velocidade_movimento * self.__direcao, 0)
        
        # Chama o método update da classe pai
        super().update(movement)
        
        # Verifica colisão com o jogador
        if self.__colidir_com_jogador():
            self.game.player.receber_dano(self.__dano)
    
    def renderizar(self, surf, offset=(0, 0)):
        """Renderiza o inimigo na tela"""
        if not self.__ativo:
            return
            
        # Renderiza o inimigo
        surf.blit(self.game.assets[self.e_tipo], (self.pos[0] - offset[0], self.pos[1] - offset[1]))