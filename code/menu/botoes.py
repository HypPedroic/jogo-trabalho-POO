import pygame

class Botao:
    def __init__(self, texto, x, y, largura, altura, cor_base, cor_hover, acao=None, borda_raio=12):
        self.texto = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_base = cor_base
        self.cor_hover = cor_hover
        self.cor_atual = cor_base
        self.acao = acao
        self.borda_raio = borda_raio
        self.fonte = pygame.font.Font("assets/fonts/PixelifySans.ttf", 32) if pygame.font.get_fonts().count("pixelifysans") else pygame.font.SysFont("Arial", 32)
        self.sombra = (0, 0, 0, 150)
        self.clicando = False
        self.som_clique = pygame.mixer.Sound("assets/sounds/clique.wav") if pygame.mixer.get_init() else None
        
    def desenhar(self, screen):
        # Sombra
        sombra_rect = self.rect.move(4, 4)
        pygame.draw.rect(screen, self.sombra, sombra_rect, border_radius=self.borda_raio)
        
        # Botão
        pygame.draw.rect(screen, self.cor_atual, self.rect, border_radius=self.borda_raio)
        
        # Texto com borda
        texto = self.fonte.render(self.texto, True, (245, 245, 245))
        borda = self.fonte.render(self.texto, True, (50, 50, 50))
        
        pos_texto = texto.get_rect(center=self.rect.center)
        screen.blit(borda, pos_texto.move(2, 2))
        screen.blit(texto, pos_texto)
        
        # Efeito de clique
        if self.clicando:
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 80))
            screen.blit(overlay, self.rect)
    
    def tratar_evento(self, event):
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)
        
        self.cor_atual = self.cor_hover if hover else self.cor_base
        
        if hover and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.clicando = True
            if self.som_clique:
                self.som_clique.play()
            pygame.time.delay(100)  # Pequeno delay para feedback
            if self.acao:
                self.acao()
        else:
            self.clicando = False