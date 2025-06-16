# Importando as bibliotecas necessárias
import pygame
import math
import random
from entidades.inimigo import Inimigo
from entidades.projetil import Projetil

# Classe para inimigos suicidas
class InimigoSuicida(Inimigo):
    def __init__(self, game, pos):
        super().__init__(game, 'inimigo_suicida', pos, (32, 32), vida=1)
        self.__velocidade_movimento = 1.5  # Velocidade inicial aumentada
        self.__velocidade_corrida = 5.0  # Velocidade quando detecta o jogador aumentada
        self.__distancia_deteccao = 250  # Distância para detectar o jogador aumentada
        self.__animacao_frame = 0
        self.__animacao_velocidade = 0.2  # Velocidade de animação aumentada
        self.__direcao_sprite = 1  # 1 para direita, -1 para esquerda
        self.__estado = 'parado'  # 'parado', 'correndo', 'explodindo'
        self.__tempo_explosao = 0
        self.__duracao_explosao = 30  # Duração da animação de explosão em frames
        self.__raio_explosao = 64  # Raio da explosão aumentado
        self.__dano_explosao = 2  # Dano causado pela explosão
        self.__detectou_jogador = False  # Flag para indicar se detectou o jogador
    
    def explodir(self):
        """Método para o inimigo suicida explodir"""
        if self.__estado != 'explodindo':
            self.__estado = 'explodindo'
            self.__tempo_explosao = 0
            self.__animacao_frame = 0
            
            # Verifica se o jogador está dentro do raio da explosão
            jogador_pos = self.game.player.pos
            jogador_centro = [
                jogador_pos[0] + self.game.player.tamanho[0] / 2,
                jogador_pos[1] + self.game.player.tamanho[1] / 2
            ]
            
            inimigo_centro = [
                self.pos[0] + self.tamanho[0] / 2,
                self.pos[1] + self.tamanho[1] / 2
            ]
            
            dx = jogador_centro[0] - inimigo_centro[0]
            dy = jogador_centro[1] - inimigo_centro[1]
            distancia = math.sqrt(dx*dx + dy*dy)
            
            if distancia <= self.__raio_explosao:
                # Aplica dano ao jogador baseado na distância (quanto mais perto, mais dano)
                fator_distancia = 1 - (distancia / self.__raio_explosao)
                dano_aplicado = max(1, int(self.__dano_explosao * fator_distancia))
                self.game.player.receber_dano(dano_aplicado)
    
    def update(self, movement=(0, 0)):
        """Atualiza o estado do inimigo suicida"""
        if not self.ativo:
            return
        
        # Se estiver explodindo, apenas atualiza a animação
        if self.__estado == 'explodindo':
            self.__tempo_explosao += 1
            self.__animacao_frame += self.__animacao_velocidade
            
            # Desativa o inimigo após a animação de explosão
            if self.__tempo_explosao >= self.__duracao_explosao:
                self.ativo = False
            return
        
        # Verifica se detectou o jogador
        if self.detectar_jogador():
            if not self.__detectou_jogador:
                self.__detectou_jogador = True
                self.__estado = 'correndo'
            
            # Calcula a direção para o jogador
            jogador_pos = self.game.player.pos
            dx = jogador_pos[0] - self.pos[0]
            
            # Atualiza a direção do sprite
            self.__direcao_sprite = 1 if dx > 0 else -1
            
            # Move rapidamente em direção ao jogador
            movement = (self.__velocidade_corrida * self.__direcao_sprite, 0)
        else:
            # Comportamento de patrulha quando não detecta o jogador
            self.__detectou_jogador = False
            self.__estado = 'parado'
            
            if self.colisoes['esquerda'] or self.colisoes['direita']:
                self.__direcao *= -1
            
            self.__direcao_sprite = self.__direcao
            movement = (self.__velocidade_movimento * self.__direcao, 0)
        
        # Atualiza o frame da animação
        self.__animacao_frame += self.__animacao_velocidade
        if self.__animacao_frame >= len(self.game.assets[self.e_tipo][self.__estado]):
            self.__animacao_frame = 0
        
        # Chama o método update da classe pai para movimento e colisões
        super().update(movement)
        
        # Verifica colisão com o jogador
        if self.colidir_com_jogador():
            self.explodir()
    
    def renderizar(self, surf, offset=(0, 0)):
        """Renderiza o inimigo suicida na tela"""
        if not self.ativo:
            return
        
        # Obtém o frame atual da animação
        frame = int(self.__animacao_frame)
        
        # Verifica se o índice está dentro dos limites
        if frame >= len(self.game.assets[self.e_tipo][self.__estado]):
            frame = 0
            
        imagem = self.game.assets[self.e_tipo][self.__estado][frame]
        
        # Inverte a imagem se necessário
        if self.__direcao_sprite == -1:
            imagem = pygame.transform.flip(imagem, True, False)
        
        # Renderiza o inimigo
        surf.blit(imagem, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        
        # Renderiza o efeito de explosão
        if self.__estado == 'explodindo':
            # Calcula o raio atual da explosão (cresce e depois diminui)
            progresso = self.__tempo_explosao / self.__duracao_explosao
            if progresso <= 0.5:
                raio_atual = int(self.__raio_explosao * (progresso * 2))
            else:
                raio_atual = int(self.__raio_explosao * ((1 - progresso) * 2))
            
            # Desenha o círculo da explosão
            centro_x = int(self.pos[0] + self.tamanho[0]/2 - offset[0])
            centro_y = int(self.pos[1] + self.tamanho[1]/2 - offset[1])
            pygame.draw.circle(surf, (255, 100, 0), (centro_x, centro_y), raio_atual)
            pygame.draw.circle(surf, (255, 200, 0), (centro_x, centro_y), raio_atual // 2)
        # Renderiza o raio da explosão durante a explosão (apenas para debug)
        # if self._estado == 'explodindo':
        #     pygame.draw.circle(surf, (255, 0, 0, 128), 
        #                       (int(self.pos[0] + self.tamanho[0]/2 - offset[0]), 
        #                        int(self.pos[1] + self.tamanho[1]/2 - offset[1])), 
        #                       self._raio_explosao, 1)