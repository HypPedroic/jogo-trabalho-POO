# Importanto as biblioteces necessárias
import pygame
import sys


# Importando as classes necessárias
from entidades.player import Player
from tilemap.tile_map import TileMap
from background.background import Background
#from menu.menu_principal import MenuPrincipal



# Classe do jogo
class Jogo:

    # Inicializando o jogo  
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((832, 640))
        self.display = pygame.Surface((624, 480))
        pygame.display.set_caption("Jogo")
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera = [0, 0]
        
        #self.menu = MenuPrincipal(self.screen)
        self.estado = "jogando"

        self.player = Player((0, 0), (20, 32))

        self.tilemap = TileMap(32)
        try:
            self.tilemap.load('data/mapas/map.json')
        except FileNotFoundError:
            pass


        # Inicializando o background
        self.background = Background(self.screen.get_height())
        
        # Carregando um background existente ou criando um novo
        try:
            self.background = Background.load('data/backgrounds/default.json')
        except FileNotFoundError:
            pass

    def inicializar_jogo(self):
        self.estado = "jogando"

    def rodar_jogo(self):
        self.display.fill((52, 222, 235))

        self.camera[0] += (self.player.retangulo().centerx - self.display.get_width() / 2 - self.camera[0]) / 16
        self.camera[1] += (self.player.retangulo().centery - self.display.get_height() / 2 - self.camera[1]) / 16
        camera_movement = (int(self.camera[0]), int(self.camera[1]))

            
        # Atualiza e renderiza o background
        self.background.update(self.camera)
        self.background.render(self.display)

        self.tilemap.renderizar(self.display, offset=camera_movement)

            
        self.player.update(self.tilemap)
        self.player.renderizar(self.display, offset=camera_movement)

        print(self.tilemap.fisica_rect_around(self.player.pos))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.mover_direita(True)
                elif event.key == pygame.K_LEFT:
                    self.player.mover_esquerda(True)
                if event.key == pygame.K_UP:
                    self.player.pular()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.mover_direita(False)
                elif event.key == pygame.K_LEFT:
                    self.player.mover_esquerda(False)

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while self.running:

            if self.estado == "menu":
                #self.menu.run()
                pass
            elif self.estado == "jogando":
                self.rodar_jogo()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()
