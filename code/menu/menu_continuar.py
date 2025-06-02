import pygame
import pickle
from .botoes import Botao

class MenuContinuar:
    def __init__(self, screen):
        self.screen = screen
        self.fonte = pygame.font.SysFont("Arial", 36)
        self.cor_fundo = (40, 40, 50)
        self.botao_voltar = Botao("Voltar", 300, 400, 200, 50, (150, 150, 150), self.voltar)

    def carregar_save(self):
        try:
            with open("save.dat", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    def continuar_jogo(self):
        save = self.carregar_save()
        if save:
            print("Jogo carregado!")  # Substitua pela lógica do seu jogo
        else:
            print("Nenhum save encontrado!")

    def voltar(self):
        from .menu_principal import MenuPrincipal
        MenuPrincipal(self.screen).run()

    def run(self):
        self.continuar_jogo()  # Tenta carregar o save diretamente