# Importando as bibliotecas necessárias
import pygame
import math
from entidades.inimigo import Inimigo
from entidades.projetil import Projetil

# Classe para inimigos terrestres
class InimigoTerrestre(Inimigo):
    def __init__(self, game, pos):
        super().__init__(game, 'inimigo_terrestre', pos, (32, 32), vida=2)
        self._velocidade_movimento = 1
        self._alcance_ataque = 300  # Distância máxima para atacar o jogador
        self._dano_projetil = 1
        self._estado = 'parado'  # 'parado', 'correndo', 'atacando'
        self._animacao_frame = 0
        self._animacao_velocidade = 0.1
        self._direcao_sprite = 1  # 1 para direita, -1 para esquerda
    
    def atacar(self):
        """Método para o inimigo terrestre atacar (atirar)"""
        if self._tempo_ataque >= self._intervalo_ataque:
            # Calcula a direção para o jogador
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
            
            # Normaliza o vetor de direção
            distancia = math.sqrt(dx*dx + dy*dy)
            if distancia > 0:
                dx /= distancia
                dy /= distancia
            
            # Cria um novo projétil
            velocidade_projetil = 3
            self.game.projeteis.append(
                Projetil(
                    self.game,
                    'projetil_inimigo',
                    inimigo_centro,
                    (10, 10),
                    [dx * velocidade_projetil, dy * velocidade_projetil],
                    origem='inimigo'
                )
            )
            
            # Reseta o tempo de ataque
            self._tempo_ataque = 0
    
    def update(self, movement=(0, 0)):
        """Atualiza o estado do inimigo terrestre"""
        if not self._ativo:
            return
        
        # Incrementa o tempo desde o último ataque
        self._tempo_ataque += 1
        
        # Atualiza o frame da animação
        self._animacao_frame += self._animacao_velocidade
        if self._animacao_frame >= len(self.game.assets[self.e_tipo]):
            self._animacao_frame = 0
        
        # Verifica se o jogador está próximo para atacar
        if self.detectar_jogador():
            jogador_pos = self.game.player.pos
            dx = jogador_pos[0] - self.pos[0]
            dy = jogador_pos[1] - self.pos[1]
            distancia = math.sqrt(dx*dx + dy*dy)
            
            # Atualiza a direção do sprite
            self._direcao_sprite = 1 if dx > 0 else -1
            
            if distancia <= self._alcance_ataque:
                # Para de se mover e ataca
                movement = (0, 0)
                self.atacar()
            else:
                # Move em direção ao jogador
                movement = (self._velocidade_movimento * self._direcao, 0)
        else:
            # Comportamento de patrulha quando não detecta o jogador
            if self.colisoes['esquerda'] or self.colisoes['direita']:
                self._direcao *= -1
            
            self._direcao_sprite = self._direcao
            movement = (self._velocidade_movimento * self._direcao, 0)
        
        # Chama o método update da classe pai
        super().update(movement)
    
    def renderizar(self, surf, offset=(0, 0)):
        """Renderiza o inimigo na tela"""
        if not self._ativo:
            return
            
        # Obtém o frame atual da animação
        frame = int(self._animacao_frame)
        if frame >= len(self.game.assets[self.e_tipo][self._estado]):
            frame = 0
            
        imagem = self.game.assets[self.e_tipo][self._estado][frame]
        
        # Inverte a imagem se o inimigo estiver indo para a esquerda
        if self._direcao == -1:
            imagem = pygame.transform.flip(imagem, True, False)
        
        # Renderiza o inimigo
        surf.blit(imagem, (self.pos[0] - offset[0], self.pos[1] - offset[1]))