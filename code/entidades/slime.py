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
        self.assets = {
            'idle': Animation(load_images('inimigos/slime/idle'), img_dur=12),
            'andar': Animation(load_images('inimigos/slime/andar'), img_dur=8),
            'ataque': Animation(load_images('inimigos/slime/ataque'), img_dur=6),
            'morrer': Animation(load_images('inimigos/slime/morrer'), img_dur=10),
        }
        
        # Chamando o construtor da classe pai
        super().__init__(self.assets, pos, tamanho)
        
        # Atributos específicos do slime
        self._vida = 1  # Slime morre com 1 hit
        self._vida_maxima = 1
        self._dano = 1
        self._estado = 'patrulhando'  # patrulhando, perseguindo, atacando, morto
        self._direcao = random.choice([-1, 1])  # -1 esquerda, 1 direita
        
        # Velocidades
        self._velocidade_patrulha = 0.3
        self._velocidade_perseguicao = 0.6
        
        # Alcances
        self._alcance_deteccao = 80
        self._alcance_ataque = 20
        
        # Timers
        self._tempo_ataque = 0
        self._intervalo_ataque = 60  # 1 segundo entre ataques
        self._tempo_patrulha = 0
        self._intervalo_mudanca_direcao = 120  # 2 segundos para mudar direção
        
        # Detecção de bordas
        self._distancia_deteccao_borda = 32
        
        # iFrames para evitar múltiplos danos
        self._iframes = 0
        self._duracao_iframes = 30
        
        # Animação de morte
        self._tempo_animacao_morte = 0
        self._duracao_animacao_morte = 60
        
        # Referências
        self.tilemap = None
        self.player = None

    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        self._vida = valor
        if self._vida <= 0:
            self._estado = 'morto'
            self._tempo_animacao_morte = 0

    @property
    def dano(self):
        return self._dano
        
    @property
    def estado(self):
        return self._estado
        
    @estado.setter
    def estado(self, valor):
        self._estado = valor
        
    @property
    def animacao_morte_completa(self):
        """Verifica se a animação de morte foi completada"""
        return self._estado == 'morto' and self._tempo_animacao_morte >= self._duracao_animacao_morte
    
    def receber_dano(self, dano):
        """Aplica dano ao slime"""
        if self._iframes <= 0 and self._estado != 'morto':
            self.vida -= dano
            self._iframes = self._duracao_iframes
            
            # Verifica se morreu
            if self.vida <= 0:
                self._estado = 'morto'
                self._tempo_animacao_morte = 0
                self.set_action('morrer')
                
            return True
        return False
    
    def detectar_jogador(self):
        """Verifica se o jogador está no alcance de detecção"""
        if not self.player or self._estado == 'morto':
            return False
        
        distancia = math.sqrt(
            (self.player.pos[0] - self.pos[0]) ** 2 + 
            (self.player.pos[1] - self.pos[1]) ** 2
        )
        
        return distancia <= self._alcance_deteccao
    
    def pode_atacar_jogador(self):
        """Verifica se pode atacar o jogador"""
        if not self.player or self._estado == 'morto':
            return False
        
        distancia = math.sqrt(
            (self.player.pos[0] - self.pos[0]) ** 2 + 
            (self.player.pos[1] - self.pos[1]) ** 2
        )
        
        return distancia <= self._alcance_ataque and self._tempo_ataque <= 0
    
    def detectar_borda(self):
        """Detecta se há uma borda à frente"""
        if not self.tilemap:
            return False
        
        # Posição à frente do slime
        pos_frente_x = self.pos[0] + (self._direcao * self._distancia_deteccao_borda)
        pos_frente_y = self.pos[1] + self.tamanho[1]  # Abaixo do slime
        
        # Verifica se há chão à frente
        tiles_frente = self.tilemap.tiles_around((pos_frente_x, pos_frente_y))
        
        # Se não há tiles sólidos abaixo, é uma borda
        for tile in tiles_frente:
            if tile['type'] in self.tilemap.FISICA_ATIVADA:
                tile_rect = pygame.Rect(
                    tile['pos'][0], tile['pos'][1],
                    self.tilemap.tile_size, self.tilemap.tile_size
                )
                if tile_rect.collidepoint(pos_frente_x, pos_frente_y):
                    return False
        
        return True  # É uma borda
    
    def mover_para_jogador(self):
        """Move o slime em direção ao jogador"""
        if not self.player:
            return
        
        # Calcula direção para o jogador
        if self.player.pos[0] > self.pos[0]:
            self._direcao = 1
            self.flip = False
        else:
            self._direcao = -1
            self.flip = True
        
        # Move na direção do jogador
        self.velocidade[0] = self._direcao * self._velocidade_perseguicao
    
    def patrulhar(self):
        """Movimento de patrulha"""
        # Verifica se deve mudar de direção
        if self._tempo_patrulha <= 0 or self.detectar_borda():
            self._direcao *= -1
            self._tempo_patrulha = self._intervalo_mudanca_direcao
            self.flip = self._direcao < 0
        
        # Move na direção atual
        self.velocidade[0] = self._direcao * self._velocidade_patrulha
        self._tempo_patrulha -= 1
    
    def atacar_jogador(self):
        """Ataca o jogador se estiver no alcance"""
        if self.pode_atacar_jogador():
            self._estado = 'atacando'
            self._tempo_ataque = self._intervalo_ataque
            
            # Aplica dano ao jogador
            if hasattr(self.player, 'receber_dano'):
                self.player.receber_dano(self._dano)
    
    def update(self, tilemap, player):
        """Atualiza o slime"""
        self.tilemap = tilemap
        self.player = player
        
        # Atualiza iframes
        if self._iframes > 0:
            self._iframes -= 1
        
        # Atualiza timer de ataque
        if self._tempo_ataque > 0:
            self._tempo_ataque -= 1
        
        # Se está morto, apenas atualiza animação de morte
        if self._estado == 'morto':
            self._tempo_animacao_morte += 1
            if self._tempo_animacao_morte >= self._duracao_animacao_morte:
                return False  # Indica que deve ser removido
            self.set_action('morrer')
            return True
        
        # Lógica de IA baseada no estado
        if self.detectar_jogador():
            if self.pode_atacar_jogador():
                self._estado = 'atacando'
                self.atacar_jogador()
                self.velocidade[0] = 0  # Para durante o ataque
                self.set_action('ataque')
            else:
                self._estado = 'perseguindo'
                self.mover_para_jogador()
                self.set_action('andar')
        else:
            self._estado = 'patrulhando'
            self.patrulhar()
            # Define animação baseada no movimento
            if abs(self.velocidade[0]) > 0.1:
                self.set_action('andar')
            else:
                self.set_action('idle')
        
        # Garante que a animação correta seja aplicada baseada no estado atual
        if self._estado == 'atacando' and self._tempo_ataque > 0:
            self.set_action('ataque')
        elif self._estado == 'perseguindo' or (self._estado == 'patrulhando' and abs(self.velocidade[0]) > 0.1):
            self.set_action('andar')
        elif self._estado == 'patrulhando' and abs(self.velocidade[0]) <= 0.1:
            self.set_action('idle')
        
        # Atualiza física
        super().update(tilemap)
        
        return True
    
    def render(self, surf, offset=(0, 0)):
        """Renderiza o slime"""
        if self._estado == 'morto' and self._tempo_animacao_morte >= self._duracao_animacao_morte:
            return  # Não renderiza se a animação de morte terminou
        
        # Efeito de piscar durante iframes
        if self._iframes > 0 and self._iframes % 6 < 3:
            return  # Pisca não renderizando
        
        super().renderizar(surf, offset)