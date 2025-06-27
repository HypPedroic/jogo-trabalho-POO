# Importando as bibliotecas necessárias
import pygame
import random
import math
from .entidade import Entidade
from utils.utils import load_images
from animation.animation import Animation

class Slime(Entidade):
    def __init__(self, pos, tamanho, game=None):
        # Carregando os assets do slime
        self.__assets = {
            'idle': Animation(load_images('inimigos/slime/idle'), img_dur=24),
            'andar': Animation(load_images('inimigos/slime/andar'), img_dur=8),
            'ataque': Animation(load_images('inimigos/slime/ataque'), img_dur=6),
            'morrer': Animation(load_images('inimigos/slime/morrer'), img_dur=10),
        }
        
        # Chamando o construtor da classe pai
        super().__init__(self.__assets, pos, tamanho)
        
        self.anim_offeset = [0, -8]  # Offset da animação para alinhar com o sprite
        
        # Atributos específicos do slime
        self.__vida = 2  # Slime morre com 2 hits
        self.__vida_maxima = 2
        self.__dano = 1
        self.__estado = 'patrulhando'  # patrulhando, perseguindo, atacando, morto
        self.__direcao = random.choice([-1, 1])  # -1 esquerda, 1 direita
        self.__game = game
        
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
        
    @property
    def game(self):
        return self.__game
    
    @game.setter
    def game(self, valor):
        self.__game = valor
        
    @property
    def vida_maxima(self):
        return self.__vida_maxima

    @vida_maxima.setter
    def vida_maxima(self, valor):
        self.__vida_maxima = valor

    @property
    def direcao(self):
        return self.__direcao

    @direcao.setter
    def direcao(self, valor):
        self.__direcao = valor

    @property
    def velocidade_patrulha(self):
        return self.__velocidade_patrulha

    @velocidade_patrulha.setter
    def velocidade_patrulha(self, valor):
        self.__velocidade_patrulha = valor

    @property
    def velocidade_perseguicao(self):
        return self.__velocidade_perseguicao

    @velocidade_perseguicao.setter
    def velocidade_perseguicao(self, valor):
        self.__velocidade_perseguicao = valor

    @property
    def alcance_deteccao(self):
        return self.__alcance_deteccao

    @alcance_deteccao.setter
    def alcance_deteccao(self, valor):
        self.__alcance_deteccao = valor

    @property
    def alcance_ataque(self):
        return self.__alcance_ataque

    @alcance_ataque.setter
    def alcance_ataque(self, valor):
        self.__alcance_ataque = valor

    @property
    def tempo_ataque(self):
        return self.__tempo_ataque

    @tempo_ataque.setter
    def tempo_ataque(self, valor):
        self.__tempo_ataque = valor

    @property
    def intervalo_ataque(self):
        return self.__intervalo_ataque

    @intervalo_ataque.setter
    def intervalo_ataque(self, valor):
        self.__intervalo_ataque = valor

    @property
    def tempo_patrulha(self):
        return self.__tempo_patrulha

    @tempo_patrulha.setter
    def tempo_patrulha(self, valor):
        self.__tempo_patrulha = valor

    @property
    def intervalo_mudanca_direcao(self):
        return self.__intervalo_mudanca_direcao

    @intervalo_mudanca_direcao.setter
    def intervalo_mudanca_direcao(self, valor):
        self.__intervalo_mudanca_direcao = valor

    @property
    def distancia_deteccao_borda(self):
        return self.__distancia_deteccao_borda

    @distancia_deteccao_borda.setter
    def distancia_deteccao_borda(self, valor):
        self.__distancia_deteccao_borda = valor

    @property
    def iframes(self):
        return self.__iframes

    @iframes.setter
    def iframes(self, valor):
        self.__iframes = valor

    @property
    def duracao_iframes(self):
        return self.__duracao_iframes

    @duracao_iframes.setter
    def duracao_iframes(self, valor):
        self.__duracao_iframes = valor

    @property
    def tempo_animacao_morte(self):
        return self.__tempo_animacao_morte

    @tempo_animacao_morte.setter
    def tempo_animacao_morte(self, valor):
        self.__tempo_animacao_morte = valor

    @property
    def duracao_animacao_morte(self):
        return self.__duracao_animacao_morte

    @duracao_animacao_morte.setter
    def duracao_animacao_morte(self, valor):
        self.__duracao_animacao_morte = valor

    @property
    def tilemap(self):
        return self.__tilemap

    @tilemap.setter
    def tilemap(self, valor):
        self.__tilemap = valor

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, valor):
        self.__player = valor
    
    def pode_atacar_jogador_colisao(self):
        """Verifica se o slime pode atacar o jogador"""
        return self.estado != 'morto' and self.iframes == 0
    
    def atacar_jogador_colisao(self, game=None):
        """Ataca o jogador causando dano"""
        if self.pode_atacar_jogador_colisao():
            self.player.receber_dano(self.dano)
            self.iframes = self.duracao_iframes
            if game:
                game.tocar_som('dano')
        
    @property
    def animacao_morte_completa(self):
        """Verifica se a animação de morte foi completada"""
        return self.estado == 'morto' and self.tempo_animacao_morte >= self.duracao_animacao_morte
    
    def reset(self):
        """Reseta o slime para estado inicial para reuso na pool"""
        self.vida = self.vida_maxima
        self.estado = 'patrulhando'
        self.direcao = random.choice([-1, 1])
        self.tempo_ataque = 0
        self.tempo_patrulha = 0
        self.iframes = 0
        self.tempo_animacao_morte = 0
        
    
    def receber_dano(self, dano):
        """Aplica dano ao slime"""
        if self.iframes <= 0 and self.estado != 'morto':
            self.vida -= dano
            self.iframes = self.duracao_iframes
            
            # Verifica se morreu
            if self.vida <= 0:
                self.estado = 'morto'
                self.tempo_animacao_morte = 0
                self.set_action('morrer')
                
            return True
        return False
    
    def __detectar_jogador(self):
        """Verifica se o jogador está no alcance de detecção"""
        if not self.player or self.estado == 'morto':
            return False
        
        distancia = math.sqrt(
            (self.player.pos[0] - self.pos[0]) ** 2 + 
            (self.player.pos[1] - self.pos[1]) ** 2
        )
        
        return distancia <= self.alcance_deteccao
    
    def __pode_atacar_jogador(self):
        """Verifica se pode atacar o jogador"""
        if not self.player or self.estado == 'morto':
            return False
        
        distancia = math.sqrt(
            (self.player.pos[0] - self.pos[0]) ** 2 + 
            (self.player.pos[1] - self.pos[1]) ** 2
        )
        
        return distancia <= self.alcance_ataque and self.tempo_ataque <= 0
    
    def __detectar_borda(self):
        """Detecta se há uma borda à frente"""
        if not self.tilemap:
            return False
        
        # Posição à frente do slime
        pos_frente_x = self.pos[0] + (self.direcao * self.distancia_deteccao_borda)
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
    
    def __mover_para_jogador(self):
        """Move o slime em direção ao jogador"""
        if not self.player:
            return
        
        # Calcula direção para o jogador
        if self.player.pos[0] > self.pos[0]:
            self.direcao = 1
            self.flip = True
        else:
            self.direcao = -1
            self.flip = False
        
        # Move na direção do jogador e muda a animação para ataque
        self.velocidade[0] = self.direcao * self.velocidade_perseguicao
        self.set_action('ataque')
    
    def __patrulhar(self):
        """Movimento de patrulha"""
        # Verifica se deve mudar de direção
        if self.tempo_patrulha <= 0 or self.__detectar_borda():
            self.direcao *= -1
            self.tempo_patrulha = self.intervalo_mudanca_direcao
            self.flip = self.direcao > 0
        
        # Move na direção atual e atualiza animação
        self.velocidade[0] = self.direcao * self.velocidade_patrulha
        self.tempo_patrulha -= 1
    
    def atacar_jogador(self, game=None):
        """Ataca o jogador se estiver no alcance"""
        if self.__pode_atacar_jogador():
            self.estado = 'atacando'
            self.tempo_ataque = self.intervalo_ataque
            
            # Toca som de ataque
            if game:
                game.tocar_som('ataque')
            
            # Aplica dano ao jogador
            if hasattr(self.player, 'receber_dano'):
                if game:
                    self.player.receber_dano(self.dano, game)
                else:
                    self.player.receber_dano(self.dano)
    
    def update(self, tilemap, player):
        """Atualiza o slime"""
        self.tilemap = tilemap
        self.player = player
        
        # Atualiza iframes
        if self.iframes > 0:
            self.iframes -= 1
        
        # Atualiza timer de ataque
        if self.tempo_ataque > 0:
            self.tempo_ataque -= 1
        
        # Se está morto, apenas atualiza animação de morte
        if self.estado == 'morto':
            self.tempo_animacao_morte += 1
            if self.tempo_animacao_morte >= self.duracao_animacao_morte:
                return False  # Indica que deve ser removido
            self.set_action('morrer')
            return True
        
        # Lógica de IA baseada no estado
        if self.__detectar_jogador():
            if self.__pode_atacar_jogador():
                self.estado = 'atacando'
                self.velocidade[0] = 0  # Para durante o ataque
                self.set_action('ataque')
            else:
                self.estado = 'perseguindo'
                self.__mover_para_jogador()
        else:
            self.estado = 'patrulhando'
            self.__patrulhar()
            self.set_action('andar')
        
        # Atualiza física e colisões
        super().update(tilemap)
        return True
    

    def renderizar(self, surf, offset=...):
        if self.iframes > 0 and (self.iframes // 3) % 2 == 0:
            return 
        super().renderizar(surf, offset)
        
        