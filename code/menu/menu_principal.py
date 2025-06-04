import pygame
import os
from .botoes import Botao

class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        self.largura, self.altura = screen.get_size()
        self.fonte_titulo = pygame.font.Font("assets/fonts/PixelifySans.ttf", 64) if pygame.font.get_fonts().count("pixelifysans") else pygame.font.SysFont("Arial", 64, bold=True)
        self.cor_fundo = (28, 25, 38)
        self.titulo = "EPIC QUEST"
        self.subtitulo = "v1.0"
        
        # Carrega background
        self.background = pygame.image.load("assets/images/menu_bg.jpg").convert() if os.path.exists("assets/images/menu_bg.jpg") else None
        if self.background:
            self.background = pygame.transform.scale(self.background, (self.largura, self.altura))
        
        # Cores dos botões (base, hover)
        self.botoes = [
            Botao("NOVO JOGO", self.largura//2 - 150, 220, 300, 60, 
                 (46, 125, 50), (69, 188, 75), self.abrir_jogar),
            Botao("CONTINUAR", self.largura//2 - 150, 300, 300, 60, 
                 (193, 126, 31), (232, 151, 38), self.abrir_continuar),
            Botao("CONFIGURAÇÕES", self.largura//2 - 150, 380, 300, 60, 
                 (51, 103, 145), (61, 124, 174), self.abrir_config),
            Botao("SAIR", self.largura//2 - 150, 460, 300, 60, 
                 (158, 47, 47), (190, 57, 57), self.sair)
        ]

        # Efeitos
        self.alpha = 0
        self.fade_surface = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.musica_menu = "assets/music/menu_theme.ogg" if os.path.exists("assets/music/menu_theme.ogg") else None
        
        if self.musica_menu and pygame.mixer.get_init():
            pygame.mixer.music.load(self.musica_menu)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            dt = clock.tick(60) / 1000.0  # Delta time para animações
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                for botao in self.botoes:
                    botao.tratar_evento(event)
            
            # Atualiza transição
            self.alpha = min(self.alpha + 2, 255)
            
            # Desenha fundo
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill(self.cor_fundo)
            
            # Desenha título
            titulo = self.fonte_titulo.render(self.titulo, True, (255, 215, 0))
            subtitulo = self.fonte_titulo.render(self.subtitulo, True, (200, 200, 200))
            
            self.screen.blit(titulo, (self.largura//2 - titulo.get_width()//2, 80))
            self.screen.blit(subtitulo, (self.largura//2 - subtitulo.get_width()//2, 150))
            
            # Desenha botões
            for botao in self.botoes:
                botao.desenhar(self.screen)
            
            # Fade in
            self.fade_surface.fill((0, 0, 0, 255 - self.alpha))
            self.screen.blit(self.fade_surface, (0, 0))
            
            pygame.display.flip()
    
    def abrir_jogar(self):
        from .menu_jogar import MenuJogar
        MenuJogar(self.screen).run()
    
    def abrir_continuar(self):
        from .menu_continuar import MenuContinuar
        MenuContinuar(self.screen).run()
    
    def abrir_config(self):
        from .menu_config import MenuConfig
        MenuConfig(self.screen).run()
    
    def sair(self):
        pygame.quit()
        exit()