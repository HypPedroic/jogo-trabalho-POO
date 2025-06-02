import pygame
from .botoes import Botao
from .menu_jogar import MenuJogar
from .menu_continuar import MenuContinuar
from .menu_config import MenuConfig

class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        self.fonte = pygame.font.SysFont("Arial", 36)
        self.cor_fundo = (30, 30, 40)
        
        self.botoes = [
            Botao("Jogar", 300, 150, 200, 50, (0, 200, 100), self.abrir_jogar),
            Botao("Continuar", 300, 220, 200, 50, (200, 150, 0), self.abrir_continuar),
            Botao("Configurações", 300, 290, 200, 50, (100, 100, 200), self.abrir_config),
            Botao("Sair", 300, 360, 200, 50, (200, 50, 50), self.sair)
        ]

    def abrir_jogar(self):
        MenuJogar(self.screen).run()

    def abrir_continuar(self):
        MenuContinuar(self.screen).run()

    def abrir_config(self):
        MenuConfig(self.screen).run()

    def sair(self):
        pygame.quit()
        exit()

    def run(self):
        running = True
        while running:
            self.screen.fill(self.cor_fundo)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for botao in self.botoes:
                    botao.tratar_evento(event)
            
            for botao in self.botoes:
                botao.desenhar(self.screen)
            
            pygame.display.flip()

        