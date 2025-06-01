# Importando as bibliotecas necessárias
import pygame
import math
import random
from entidades.inimigo import Inimigo
from entidades.projetil import Projetil

# Classe para o dragão voador
class Dragao(Inimigo):
    def __init__(self, game, pos):
        super().__init__(game, 'dragao', pos, (48, 48), vida=3)
        self._velocidade_movimento = 2
        self._intervalo_ataque = 120  # frames entre ataques (2 segundos a 60 FPS)
        self._amplitude_voo = 30  # Amplitude da oscilação vertical
        self._frequencia_voo = 0.02  # Frequência da oscilação
        self._tempo_voo = random.random() * 100  # Tempo inicial aleatório para variar o movimento
        self._estado = 'parado'  # 'parado', 'correndo', 'atacando'
        self._animacao_frame = 0
        self._animacao_velocidade = 0.1
        self._dano_projetil = 1
        self._altura_voo = random.randint(100, 150)  # altura aleatória para voar
        self._amplitude_voo = random.randint(10, 30)  # amplitude do movimento de voo
        self._frequencia_voo = 0.02  # frequência do movimento de voo
        self._tempo_voo = random.random() * 100  # fase inicial aleatória
        self._animacao_frame = 0
        self._animacao_velocidade = 0.1
        self._direcao_sprite = 1  # 1 para direita, -1 para esquerda
        self._altura_base = pos[1]  # altura base para o movimento de voo
        self._modo_ataque = False  # se está em modo de ataque
        self._tempo_modo_ataque = 0  # tempo no modo de ataque
        self._duracao_modo_ataque = 180  # duração do modo de ataque (3 segundos)
    
    def atacar(self):
        """Método para o dragão atacar (soltar fogo)"""
        if self._tempo_ataque >= self._intervalo_ataque and self._modo_ataque:
            # Cria um novo projétil de fogo que cai verticalmente
            posicao_fogo = [self.pos[0] + self.tamanho[0] / 2 - 10, self.pos[1] + self.tamanho[1]]
            
            self.game.projeteis.append(
                Projetil(
                    self.game,
                    'fogo_dragao',
                    posicao_fogo,
                    (20, 30),
                    [0, 4],  # velocidade vertical para baixo
                    origem='inimigo',
                    gravidade=0.1  # adiciona um pouco de gravidade para efeito realista
                )
            )
            
            # Reseta o tempo de ataque
            self._tempo_ataque = 0
    
    def update(self, initial_movement=(0, 0)):
        """Updates the dragon's state"""
        if not self._ativo:
            return
        
        self._update_timers()
        self._update_animation()
        
        movement = self._handle_movement()
        self._apply_movement(movement)
        self._check_player_collision()
        
        # Atualiza o movimento vertical de voo se não estiver em modo de ataque
        if not self._modo_ataque:
            altura_voo = self._altura_base - self._altura_voo + math.sin(self._tempo_voo * self._frequencia_voo) * self._amplitude_voo
            self.pos[1] = altura_voo
    
    def _update_timers(self):
        """Updates internal timers"""
        self._tempo_ataque += 1
        self._tempo_voo += 1
        if self._modo_ataque:
            self._tempo_modo_ataque += 1
            if self._tempo_modo_ataque >= self._duracao_modo_ataque:
                self._modo_ataque = False
    
    def _update_animation(self):
        """Updates animation frame"""
        self._animacao_frame += self._animacao_velocidade
        if self._animacao_frame >= len(self.game.assets[self.e_tipo][self._estado]):
            self._animacao_frame = 0
    
    def _handle_movement(self):
        """Handles movement logic and returns movement vector"""
        if self.detectar_jogador():
            return self._handle_player_detected()
        return self._handle_patrol()
    
    def _handle_player_detected(self):
        """Handles movement when player is detected"""
        jogador_pos = self.game.player.pos
        dx = jogador_pos[0] - self.pos[0]
        
        # Atualiza a direção do sprite
        self._direcao_sprite = 1 if dx > 0 else -1
        
        # Verifica se deve entrar em modo de ataque
        if not self._modo_ataque and abs(dx) < 50:  # se estiver aproximadamente acima do jogador
            self._modo_ataque = True
            self._tempo_modo_ataque = 0
        
        if self._modo_ataque:
            # Fica parado acima do jogador e ataca
            self.atacar()
            return (0, 0)  # Não se move quando está atacando
        else:
            # Move em direção ao jogador
            return (self._velocidade_movimento * self._direcao_sprite, 0)
    
    def _handle_patrol(self):
        """Handles patrol movement when player is not detected"""
        # Comportamento de patrulha quando não detecta o jogador
        if self._colisoes['esquerda'] or self._colisoes['direita']:
            self._direcao *= -1
        
        self._direcao_sprite = self._direcao
        self._modo_ataque = False
        
        # Calcula o movimento vertical de voo (movimento senoidal)
        altura_voo = self._altura_base - self._altura_voo + math.sin(self._tempo_voo * self._frequencia_voo) * self._amplitude_voo
        self.pos[1] = altura_voo
        
        # Retorna o movimento horizontal para patrulha
        return (self._velocidade_movimento * self._direcao, 0)
    
    def _apply_movement(self, movement):
        """Applies movement and handles collisions"""
        # Reseta as colisões
        self._colisoes = {'cima': False, 'baixo': False, 'esquerda': False, 'direita': False}
        
        # Movimento horizontal
        frame_movement = (movement[0] + self._velocidade[0], 0)
        self._pos[0] += frame_movement[0]
        
        # Verifica colisões horizontais
        retangulo_colisao = self.retangulo()
        for rect in self.game.tilemap.fisica_rect_around(self._pos):
            if retangulo_colisao.colliderect(rect):
                if frame_movement[0] > 0:
                    retangulo_colisao.right = rect.left
                    self._colisoes['direita'] = True
                if frame_movement[0] < 0:
                    retangulo_colisao.left = rect.right
                    self._colisoes['esquerda'] = True
                self._pos[0] = retangulo_colisao.x
    
    def _check_player_collision(self):
        """Checks for collision with the player"""
        if self.colidir_com_jogador():
            self.game.player.receber_dano(self._dano)
    
    def renderizar(self, surf, offset=(0, 0)):
        """Renderiza o dragão na tela"""
        if not self._ativo:
            return
            
        # Obtém o frame atual da animação
        frame = int(self._animacao_frame)
        if frame >= len(self.game.assets[self.e_tipo][self._estado]):
            frame = 0
            
        imagem = self.game.assets[self.e_tipo][self._estado][frame]
        
        # Inverte a imagem se o dragão estiver indo para a esquerda
        if self._direcao == -1:
            imagem = pygame.transform.flip(imagem, True, False)
        
        # Renderiza o dragão
        surf.blit(imagem, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        
        # Renderiza uma sombra no chão
        sombra_pos = [self.pos[0] + self.tamanho[0]/4, self._altura_base + 30 - offset[1]]
        pygame.draw.ellipse(surf, (0, 0, 0, 128), [sombra_pos[0] - offset[0], sombra_pos[1], self.tamanho[0]/2, 10])