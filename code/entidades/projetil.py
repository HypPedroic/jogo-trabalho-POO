# Importando as bibliotecas necessárias
import pygame
import math

# Classe para projéteis
class Projetil:
    def __init__(self, game, tipo, pos, tamanho, velocidade, origem='jogador', dano=1, tempo_vida=180, gravidade=0):
        self.game = game
        self.tipo = tipo
        self.pos = list(pos)
        self.tamanho = tamanho
        self.velocidade = velocidade
        self.origem = origem  # 'jogador' ou 'inimigo'
        self.dano = dano
        self.tempo_vida = tempo_vida  # duração em frames
        self.tempo_atual = 0
        self.ativo = True
        self.gravidade = gravidade
        self.animacao_frame = 0
        self.animacao_velocidade = 0.2
        
        # Calcula o ângulo do projétil baseado na velocidade
        if velocidade[0] != 0 or velocidade[1] != 0:
            self.angulo = math.degrees(math.atan2(velocidade[1], velocidade[0]))
        else:
            self.angulo = 0
    
    def retangulo(self):
        """Retorna o retângulo de colisão do projétil"""
        return pygame.Rect(self.pos[0], self.pos[1], self.tamanho[0], self.tamanho[1])
    
    def update(self):
        """Atualiza o estado do projétil"""
        if not self.ativo:
            return
        
        # Incrementa o tempo de vida
        self.tempo_atual += 1
        if self.tempo_atual >= self.tempo_vida:
            self.ativo = False
            return
        
        # Atualiza o frame da animação
        self.animacao_frame += self.animacao_velocidade
        if self.animacao_frame >= len(self.game.assets[self.tipo]):
            self.animacao_frame = 0
        
        # Aplica gravidade se necessário
        if self.gravidade > 0:
            self.velocidade[1] += self.gravidade
        
        # Atualiza a posição
        self.pos[0] += self.velocidade[0]
        self.pos[1] += self.velocidade[1]
        
        # Verifica colisão com tiles
        retangulo_colisao = self.retangulo()
        for rect in self.game.tilemap.fisica_rect_around(self.pos):
            if retangulo_colisao.colliderect(rect):
                self.ativo = False
                return
        
        # Verifica colisão com entidades
        if self.origem == 'jogador':
            # Verifica colisão com inimigos
            for inimigo in self.game.inimigos:
                if inimigo.ativo and retangulo_colisao.colliderect(inimigo.retangulo()):
                    inimigo.receber_dano(self.dano)
                    self.ativo = False
                    return
        elif self.origem == 'inimigo':
            # Verifica colisão com o jogador
            if retangulo_colisao.colliderect(self.game.player.retangulo()):
                self.game.player.receber_dano(self.dano)
                self.ativo = False
                return
    
    def renderizar(self, surf, offset=(0, 0)):
        """Renderiza o projétil na tela"""
        if not self.ativo:
            return
        
        # Obtém o frame atual da animação
        frame = int(self.animacao_frame)
        imagem = self.game.assets[self.tipo][frame]
        
        # Rotaciona a imagem conforme o ângulo do projétil
        imagem_rotacionada = pygame.transform.rotate(imagem, -self.angulo)  # negativo porque pygame rotaciona no sentido anti-horário
        
        # Ajusta a posição para centralizar após a rotação
        rect_rotacionado = imagem_rotacionada.get_rect(center=(self.pos[0] + self.tamanho[0]/2, self.pos[1] + self.tamanho[1]/2))
        
        # Renderiza o projétil
        surf.blit(imagem_rotacionada, (rect_rotacionado.x - offset[0], rect_rotacionado.y - offset[1]))