# Importando as bibliotecas necessárias
import pygame
import math
from entidades.fisica_entidade import FisicaEntidade
from entidades.projetil import Projetil

# Classe para o jogador
class Jogador(FisicaEntidade):
    def __init__(self, game, pos):
        super().__init__(game, 'player', pos, (32, 32))
        self._vida = 3
        self._vida_maxima = 3
        self._velocidade_movimento = 3
        self._forca_pulo = 5  # Reduzido de 8 para 5 para um pulo mais controlado
        self._pode_pular = False
        self._pulo_duplo_disponivel = False  # Controla se o pulo duplo está disponível
        self._tempo_recarga_pulo_duplo = 0  # Tempo atual de recarga do pulo duplo
        self._recarga_maxima_pulo_duplo = 180  # 3 segundos de recarga (60 frames por segundo)
        self._tempo_invulneravel = 0
        self._duracao_invulneravel = 60  # 1 segundo de invulnerabilidade após dano
        self._animacao_frame = 0
        self._animacao_velocidade = 0.2
        self._estado = 'parado'  # 'parado', 'correndo', 'pulando', 'caindo'
        self._direcao = 1  # 1 para direita, -1 para esquerda
        self._distancia_percorrida = 0
        self._posicao_inicial_x = pos[0]
        self._tempo_ataque = 0
        self._intervalo_ataque = 30  # frames entre ataques (0.5 segundos)
        self._vivo = True
    
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, value):
        self._vida = max(0, min(value, self._vida_maxima))
        if self._vida <= 0:
            self._vivo = False
    
    @property
    def vida_maxima(self):
        return self._vida_maxima
    
    @vida_maxima.setter
    def vida_maxima(self, value):
        self._vida_maxima = value
    
    @property
    def vivo(self):
        return self._vivo
    
    @vivo.setter
    def vivo(self, value):
        self._vivo = value
    
    @property
    def distancia_percorrida(self):
        return self._distancia_percorrida
    
    @property
    def pulo_duplo_disponivel(self):
        return self._pulo_duplo_disponivel
    
    @property
    def tempo_recarga_pulo_duplo(self):
        return self._tempo_recarga_pulo_duplo
    
    @property
    def recarga_maxima_pulo_duplo(self):
        return self._recarga_maxima_pulo_duplo
    
    def receber_dano(self, dano):
        """Método para o jogador receber dano"""
        if self._tempo_invulneravel <= 0:
            self._vida -= dano
            self._tempo_invulneravel = self._duracao_invulneravel
            
            if self._vida <= 0:
                self._vivo = False
    
    def atacar(self):
        """Método para o jogador atacar (atirar)"""
        if self._tempo_ataque >= self._intervalo_ataque:
            # Posição inicial do projétil
            posicao_projetil = [
                self.pos[0] + (self.tamanho[0] if self._direcao > 0 else 0),
                self.pos[1] + self.tamanho[1] / 2 - 5
            ]
            
            # Cria um novo projétil
            self.game.projeteis.append(
                Projetil(
                    self.game,
                    'projetil_jogador',
                    posicao_projetil,
                    (10, 10),
                    [5 * self._direcao, 0],
                    origem='jogador'
                )
            )
            
            # Reseta o tempo de ataque
            self._tempo_ataque = 0
    
    def update(self, movement):
        """Atualiza o estado do jogador"""
        if not self._vivo:
            return
        
        # Incrementa o tempo desde o último ataque
        self._tempo_ataque += 1
        
        # Decrementa o tempo de invulnerabilidade
        if self._tempo_invulneravel > 0:
            self._tempo_invulneravel -= 1
        
        # Atualiza a recarga do pulo duplo
        if not self._pulo_duplo_disponivel:
            self._tempo_recarga_pulo_duplo += 1
            if self._tempo_recarga_pulo_duplo >= self._recarga_maxima_pulo_duplo:
                self._pulo_duplo_disponivel = True
                self._tempo_recarga_pulo_duplo = self._recarga_maxima_pulo_duplo
        
        # Atualiza a direção do jogador
        if movement[0] > 0:
            self._direcao = 1
        elif movement[0] < 0:
            self._direcao = -1
        
        # Aplica a velocidade de movimento
        movement = (movement[0] * self._velocidade_movimento, movement[1])
        
        # Atualiza o estado do jogador
        if self.colisoes['baixo']:
            self._pode_pular = True
            # Recarrega o pulo duplo quando tocar o chão
            self._pulo_duplo_disponivel = True
            self._tempo_recarga_pulo_duplo = self._recarga_maxima_pulo_duplo
            
            if movement[0] == 0:
                self._estado = 'parado'
            else:
                self._estado = 'correndo'
        else:
            self._pode_pular = False
            if self.velocidade[1] < 0:
                self._estado = 'pulando'
            else:
                self._estado = 'caindo'
        
        # Atualiza o frame da animação
        self._animacao_frame += self._animacao_velocidade
        if self._animacao_frame >= len(self.game.assets[self.e_tipo][self._estado]):
            self._animacao_frame = 0
        
        # Atualiza a distância percorrida
        if self.pos[0] > self._posicao_inicial_x:
            nova_distancia = self.pos[0] - self._posicao_inicial_x
            if nova_distancia > self._distancia_percorrida:
                self._distancia_percorrida = nova_distancia
        
        # Chama o método update da classe pai
        super().update(movement)
    
    def pular(self):
        """Método para o jogador pular"""
        if self._pode_pular:
            self.velocidade[1] = -self._forca_pulo
            self._pode_pular = False
        elif self._pulo_duplo_disponivel and not self._pode_pular:
            # Executa o pulo duplo
            self.velocidade[1] = -self._forca_pulo
            self._pulo_duplo_disponivel = False
            self._tempo_recarga_pulo_duplo = 0
    
    def renderizar(self, surf, offset=(0, 0)):
        """Renderiza o jogador na tela"""
        if not self._vivo:
            return
        
        # Obtém o frame atual da animação
        frame = int(self._animacao_frame)
        imagem = self.game.assets[self.e_tipo][self._estado][frame]
        
        # Inverte a imagem se necessário
        if self._direcao == -1:
            imagem = pygame.transform.flip(imagem, True, False)
        
        # Efeito de piscar quando invulnerável
        if self._tempo_invulneravel > 0 and self._tempo_invulneravel % 6 >= 3:
            # Não renderiza o jogador a cada 3 frames durante invulnerabilidade
            return
        
        # Renderiza o jogador
        surf.blit(imagem, (self.pos[0] - offset[0], self.pos[1] - offset[1]))