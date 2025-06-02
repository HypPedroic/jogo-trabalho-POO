import pygame

class Botao:
    def __init__(self, texto, x, y, largura, altura, cor, acao=None):
        self.texto = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor
        self.acao = acao
        self.fonte = pygame.font.SysFont("Arial", 24)
    
    def desenhar(self, screen):
        pygame.draw.rect(screen, self.cor, self.rect)
        texto_render = self.fonte.render(self.texto, True, (255, 255, 255))
        screen.blit(texto_render, (self.rect.x + 10, self.rect.y + 10))
    
    def tratar_evento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.acao:
                self.acao()