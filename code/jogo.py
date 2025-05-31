# Importanto as biblioteces necessárias
import pygame
import sys

# Importando as classes necessárias
from entidades.entidade import Entidade
from tilemap.tile_map import TileMap
from background.background import Background

# Importando as funções necessárias
from utils.utils import load_image, load_images

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
        
        self.movemento = [False, False]
        
        # Carregando as imagens
        self.assets = {
            'grass': load_images('tiles/grama'),
            'player': load_image('player/player.png'),
            'background': load_image('background/Background.png'),
            'Stones': load_images('Objetos/Stones'),
            'Trees': load_images('Objetos/Trees'),
            'Grama': load_images('Objetos/Grass'),
            'Boxes': load_images('Objetos/Boxes'),
            'Bushes': load_images('Objetos/Bushes'),
            'Fences': load_images('Objetos/Fence'),
            'Pointers': load_images('Objetos/Pointers'),
            'Ridges': load_images('Objetos/Ridges'),
            'Willows': load_images('Objetos/Willows'),
        }

        self.player = Entidade(self, 'player', (0, 0), (32, 32))
        self.tilemap = TileMap(self, 32)
        try:
            self.tilemap.load('data/mapas/map.json')
        except FileNotFoundError:
            pass


        self.camera = [0, 0]

        # Inicializando o background
        self.background = Background(self)
        # Adicione suas camadas aqui - exemplo:
        self.background.add_layer('background/Layers/1.png', 0.1)
        self.background.add_layer('background/Layers/2.png', 0.3)
        self.background.add_layer('background/Layers/3.png', 0.5)
        self.background.add_layer('background/Layers/4.png', 0.7)
        self.background.add_layer('background/Layers/5.png', 0.9)

    def run(self):
        while self.running:

            self.display.fill((52, 222, 235))

            self.camera[0] += (self.player.retangulo().centerx - self.display.get_width() / 2 - self.camera[0]) / 16
            self.camera[1] += (self.player.retangulo().centery - self.display.get_height() / 2 - self.camera[1]) / 16
            camera_movement = (int(self.camera[0]), int(self.camera[1]))

            
            # Atualiza e renderiza o background
            self.background.update(self.camera)
            self.background.render(self.display)

            self.tilemap.renderizar(self.display, offset=camera_movement)
            
            self.player.update((self.movemento[0] - self.movemento[1], 0))
            self.player.renderizar(self.display, offset=camera_movement)

            print(self.tilemap.fisica_rect_around(self.player.pos))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.movemento[0] = True
                    elif event.key == pygame.K_LEFT:
                        self.movemento[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocidade[1] = -5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movemento[0] = False
                    elif event.key == pygame.K_LEFT:
                        self.movemento[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()
