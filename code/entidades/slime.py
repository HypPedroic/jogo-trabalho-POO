# Importando as bibliotecas necessárias
import pygame
import random
import math
from .entidade import Entidade
from utils.utils import load_images
from utils.animation import Animation

class Slime(Entidade):
    def __init__(self, pos, tamanho):
        # Carregando os assets do slime
        self.__assets = {
            'idle': Animation(load_images('inimigos/slime/idle'), img_dur=12),
            'andar': Animation(load_images('inimigos/slime/andar'), img_dur=8),
            'ataque': Animation(load_images('inimigos/slime/ataque'), img_dur=6),
            'morrer': Animation(load_images('inimigos/slime/morrer'), img_dur=10),
        }
        
        # Chamando o construtor da classe pai
        super().__init__(self.__assets, pos, tamanho)
        
        # Atributos específicos do slime
        self.__vida = 2  # Slime morre com 2 hits
        self.__vida_maxima = 2
        self.__dano = 1
        self.__estado = 'patrulhando'  # patrulhando, perseguindo, atacando, morto
        self.__direcao = random.choice([-1, 1])  # -1 esquerda, 1 direita
        
        # Velocidades
        self.__velocidade_patrulha = 0.3
        self.__velocidade_perseguicao = 0.6
        
        # Alcances
        self.__alcance_deteccao = 80
        self.__alcance_ataque = 20
        
        # Timers
        self.__tempo_ataque = 0
        self.__intervalo_ataque = 60  # 1 segundo entre ataques
        self.__tempo_patrulha = 0
        self.__intervalo_mudanca_direcao = 120  # 2 segundos para mudar direção
        
        # Detecção de bordas
        self.__distancia_deteccao_borda = 32
        
        # iFrames para evitar múltiplos danos
        self.__iframes = 0
        self.__duracao_iframes = 30
        
        # Animação de morte
        self.__tempo_animacao_morte = 0
        self.__duracao_animacao_morte = 60
        
        # Referências
        self.__tilemap = None
        self.__player = None

    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, valor):
        self.__vida = valor
        if self.__vida <= 0:
            self.__estado = 'morto'
            self.__tempo_animacao_morte = 0

    @property
    def dano(self):
        return self.__dano
        
    @property
    def estado(self):
        return self.__estado
        
    @estado.setter
    def estado(self, valor):
        self.__estado = valor
    
    def pode_atacar_jogador(self):
        """Verifica se o slime pode atacar o jogador"""
        return self.__estado != 'morto' and self.__iframes == 0
    
    def atacar_jogador(self, game=None):
        """Ataca o jogador causando dano"""
        if self.pode_atacar_jogador():
            self.__player.receber_dano(self.__dano)
            self.__iframes = self.__duracao_iframes
            if game:
                game.tocar_som('dano')
        
    @property
    def animacao_morte_completa(self):
        """Verifica se a animação de morte foi completada"""
        return self.__estado == 'morto' and self.__tempo_animacao_morte >= self.__duracao_animacao_morte
    
    def receber_dano(self, dano):
        """Aplica dano ao slime"""
        if self.__iframes <= 0 and self.__estado != 'morto':
            self.vida -= dano
            self.__iframes = self.__duracao_iframes
            
            # Verifica se morreu
            if self.vida <= 0:
                self.__estado = 'morto'
                self.__tempo_animacao_morte = 0
                self.set_action('morrer')
                
            return True
        return False
    
    def __detectar_jogador(self):
        """Verifica se o jogador está no alcance de detecção"""
        if not self.__player or self.__estado == 'morto':
            return False
        
        distancia = math.sqrt(
            (self.__player.pos[0] - self.pos[0]) ** 2 + 
            (self.__player.pos[1] - self.pos[1]) ** 2
        )
        
        return distancia <= self.__alcance_deteccao
    
    def __pode_atacar_jogador(self):
        """Verifica se pode atacar o jogador"""
        if not self.__player or self.__estado == 'morto':
            return False
        
        distancia = math.sqrt(
            (self.__player.pos[0] - self.pos[0]) ** 2 + 
            (self.__player.pos[1] - self.pos[1]) ** 2
        )
        
        return distancia <= self.__alcance_ataque and self.__tempo_ataque <= 0
    
    def __detectar_borda(self):
        """Detecta se há uma borda à frente"""
        if not self.__tilemap:
            return False
        
        # Posição à frente do slime
        pos_frente_x = self.pos[0] + (self.__direcao * self.__distancia_deteccao_borda)
        pos_frente_y = self.pos[1] + self.tamanho[1]  # Abaixo do slime
        
        # Verifica se há chão à frente
        tiles_frente = self.__tilemap.tiles_around((pos_frente_x, pos_frente_y))
        
        # Se não há tiles sólidos abaixo, é uma borda
        for tile in tiles_frente:
            if tile['type'] in self.__tilemap.FISICA_ATIVADA:
                tile_rect = pygame.Rect(
                    tile['pos'][0], tile['pos'][1],
                    self.__tilemap.tile_size, self.__tilemap.tile_size
                )
                if tile_rect.collidepoint(pos_frente_x, pos_frente_y):
                    return False
        
        return True  # É uma borda
    
    def __mover_para_jogador(self):
        """Move o slime em direção ao jogador"""
        if not self.__player:
            return
        
        # Calcula direção para o jogador
        if self.__player.pos[0] > self.pos[0]:
            self.__direcao = 1
            self.flip = False
        else:
            self.__direcao = -1
            self.flip = True
        
        # Move na direção do jogador
        self.velocidade[0] = self.__direcao * self.__velocidade_perseguicao
    
    def __patrulhar(self):
        """Movimento de patrulha"""
        # Verifica se deve mudar de direção
        if self.__tempo_patrulha <= 0 or self.__detectar_borda():
            self.__direcao *= -1
            self.__tempo_patrulha = self.__intervalo_mudanca_direcao
            self.flip = self.__direcao < 0
        
        # Move na direção atual
        self.velocidade[0] = self.__direcao * self.__velocidade_patrulha
        self.__tempo_patrulha -= 1
    
    def __atacar_jogador(self, game=None):
        """Ataca o jogador se estiver no alcance"""
        if self.__pode_atacar_jogador():
            self.__estado = 'atacando'
            self.__tempo_ataque = self.__intervalo_ataque
            
            # Toca som de ataque
            if game:
                game.tocar_som('ataque')
            
            # Aplica dano ao jogador
            if hasattr(self.__player, 'receber_dano'):
                if game:
                    self.__player.receber_dano(self.__dano, game)
                else:
                    self.__player.receber_dano(self.__dano)
    
    def update(self, tilemap, player):
        """Atualiza o slime"""
        self.__tilemap = tilemap
        self.__player = player
        
        # Atualiza iframes
        if self.__iframes > 0:
            self.__iframes -= 1
        
        # Atualiza timer de ataque
        if self.__tempo_ataque > 0:
            self.__tempo_ataque -= 1
        
        # Se está morto, apenas atualiza animação de morte
        if self.__estado == 'morto':
            self.__tempo_animacao_morte += 1
            if self.__tempo_animacao_morte >= self.__duracao_animacao_morte:
                return False  # Indica que deve ser removido
            self.set_action('morrer')
            return True
        
        # Lógica de IA baseada no estado
        if self.__detectar_jogador():
            if self.__pode_atacar_jogador():
                self.__estado = 'atacando'
                self.velocidade[0] = 0  # Para durante o ataque
                self.set_action('ataque')
            else:
                self.__estado = 'perseguindo'
                self.__mover_para_jogador()
                self.set_action('andar')
        else:
            self.__estado = 'patrulhando'
            self.__patrulhar()
            self.set_action('andar')
        
        # Atualiza física e colisões
        super().update(tilemap)
        return True
    
    def render(self, surf, offset=(0, 0)):
        """Renderiza o slime"""
        if self.__estado == 'morto' and self.__tempo_animacao_morte >= self.__duracao_animacao_morte:
            return  # Não renderiza se a animação de morte terminou
        
        # Efeito de piscar durante iframes
        if self.__iframes > 0 and self.__iframes % 6 < 3:
            return  # Pisca não renderizando
        
        super().renderizar(surf, offset)