import pygame
from .botoes import Botao

class MenuConfig:
    def __init__(self, screen):
        self.screen = screen
        self.fonte = pygame.font.SysFont("Arial", 36)
        self.cor_fundo = (40, 40, 50)
        self.volume = 50
        self.botoes = [
            Botao("-", 250, 200, 50, 50, (100, 100, 100), self.diminuir_volume),
            Botao("+", 450, 200, 50, 50, (100, 100, 100), self.aumentar_volume),
            Botao("Voltar", 300, 400, 200, 50, (150, 150, 150), self.voltar)
        ]

    def diminuir_volume(self):
        if self.volume > 0:
            self.volume -= 10
            pygame.mixer.music.set_volume(self.volume / 100)

    def aumentar_volume(self):
        if self.volume < 100:
            self.volume += 10
            pygame.mixer.music.set_volume(self.volume / 100)

    def voltar(self):
        from .menu_principal import MenuPrincipal
        MenuPrincipal(self.screen).run()

    def run(self):
        running = True
        while running:
            self.screen.fill(self.cor_fundo)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for botao in self.botoes:
                    botao.tratar_evento(event)
            
            texto_volume = self.fonte.render(f"Volume: {self.volume}%", True, (255, 255, 255))
            self.screen.blit(texto_volume, (300, 150))
            
            for botao in self.botoes:
                botao.desenhar(self.screen)
            
            pygame.display.flip()