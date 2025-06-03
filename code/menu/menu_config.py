import pygame
from botoes import Botao

class MenuConfig:
    def __init__(self, screen):
        self.screen = screen
        self.largura, self.altura = screen.get_size()
        self.fonte = pygame.font.Font("assets/fonts/PixelifySans.ttf", 42) if pygame.font.get_fonts().count("pixelifysans") else pygame.font.SysFont("Arial", 42)
        self.fonte_pequena = pygame.font.Font(None, 28)
        self.cor_fundo = (35, 32, 48, 200)
        self.volume = 70  # Valor padrão
        self.resolucoes = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
        self.resolucao_atual = 0
        
        self.botoes = [
            Botao("-", self.largura//2 - 120, 220, 60, 50, 
                 (100, 100, 100), (130, 130, 130), self.diminuir_volume),
            Botao("+", self.largura//2 + 60, 220, 60, 50, 
                 (100, 100, 100), (130, 130, 130), self.aumentar_volume),
            Botao("RESOLUÇÃO", self.largura//2 - 150, 320, 300, 50, 
                 (80, 80, 180), (100, 100, 220), self.mudar_resolucao),
            Botao("VOLTAR", self.largura//2 - 150, 420, 300, 50, 
                 (180, 50, 50), (220, 70, 70), self.voltar)
        ]

    def diminuir_volume(self):
        if self.volume > 0:
            self.volume -= 10
            pygame.mixer.music.set_volume(self.volume / 100)

    def aumentar_volume(self):
        if self.volume < 100:
            self.volume += 10
            pygame.mixer.music.set_volume(self.volume / 100)

    def mudar_resolucao(self):
        self.resolucao_atual = (self.resolucao_atual + 1) % len(self.resolucoes)
        nova_larg, nova_alt = self.resolucoes[self.resolucao_atual]
        pygame.display.set_mode((nova_larg, nova_alt))
        self.largura, self.altura = nova_larg, nova_alt

    def voltar(self):
        from .menu_principal import MenuPrincipal
        MenuPrincipal(self.screen).run()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                for botao in self.botoes:
                    botao.tratar_evento(event)
            
            # Fundo semi-transparente
            overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            overlay.fill(self.cor_fundo)
            self.screen.blit(overlay, (0, 0))
            
            # Título
            titulo = self.fonte.render("CONFIGURAÇÕES", True, (255, 255, 255))
            self.screen.blit(titulo, (self.largura//2 - titulo.get_width()//2, 100))
            
            # Volume
            texto_volume = self.fonte_pequena.render(f"VOLUME: {self.volume}%", True, (200, 200, 200))
            self.screen.blit(texto_volume, (self.largura//2 - texto_volume.get_width()//2, 180))
            
            # Barra de volume
            pygame.draw.rect(self.screen, (70, 70, 90), (self.largura//2 - 100, 210, 200, 15))
            pygame.draw.rect(self.screen, (0, 180, 80), (self.largura//2 - 100, 210, self.volume * 2, 15))
            
            # Resolução atual
            res_text = f"{self.resolucoes[self.resolucao_atual][0]}x{self.resolucoes[self.resolucao_atual][1]}"
            texto_res = self.fonte_pequena.render(res_text, True, (200, 200, 200))
            self.screen.blit(texto_res, (self.largura//2 - texto_res.get_width()//2, 350))
            
            # Botões
            for botao in self.botoes:
                botao.desenhar(self.screen)
            
            pygame.display.flip()