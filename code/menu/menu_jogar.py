import pygame
from botoes import Botao

class MenuJogar:
    def __init__(self, screen):
        self.screen = screen
        self.fonte = pygame.font.SysFont("Arial", 36)
        self.cor_fundo = (40, 40, 50)
        self.botao_voltar = Botao("Voltar", 300, 400, 200, 50, (150, 150, 150), self.voltar)

    def iniciar_jogo(self):
        # Substitua por: "from seu_jogo import Game" (se necessário)
        print("Jogo iniciado!")  # Só para teste
        return True
    
    def voltar(self):
        from .menu_principal import MenuPrincipal
        MenuPrincipal(self.screen).run()

    def run(self):
        self.iniciar_jogo()  # Inicia o jogo diretamente