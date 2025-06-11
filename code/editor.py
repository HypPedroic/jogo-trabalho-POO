# Importanto as biblioteces necessárias
import pygame
import sys

# Importando as classes necessárias
from tilemap.tile_map import TileMap

# Importando as funções necessárias
from utils.utils import load_image, load_images

RENDER_SCALE = 2

# Classe do jogo
class Editor:

    # Inicializando o jogo
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((832, 640))
        pygame.display.set_caption("editor")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.movemento = [False, False, False, False]
        
        # Carregando as imagens
        self.assets = {
            'grass': load_images('tiles/grama'),
            'Stones': load_images('Objetos/Stones'),
            'Trees': load_images('Objetos/Trees'),
            'Grama': load_images('Objetos/Grass'),
            'Boxes': load_images('Objetos/Boxes'),
            'Bushes': load_images('Objetos/Bushes'),
            'Fences': load_images('Objetos/Fence'),
            'Pointers': load_images('Objetos/Pointers'),
            'Ridges': load_images('Objetos/Ridges'),
            'Willows': load_images('Objetos/Willows'),
            'Spawners': load_images('Objetos/spawners'),


            #'stone': load_images('tiles/pedra'),  # Adicione mais tipos de tiles aqui
        }

        self.tilemap = TileMap(32)

        try:
            self.tilemap.load('data/mapas/map.json')
        except FileNotFoundError:
            pass

        self.camera = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_click = False

        self.ongrid = True



    def run(self):
        while self.running:

            self.screen.fill((0, 0, 0))
 
            self.camera[0] += (self.movemento[0] - self.movemento[1]) * 5
            self.camera[1] += (self.movemento[3] - self.movemento[2]) * 5
            camera_render = (int(self.camera[0]), int(self.camera[1]))

            self.tilemap.renderizar(self.screen, offset=camera_render)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(120)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] - RENDER_SCALE, mpos[1] - RENDER_SCALE)
            tile_pos =(int(mpos[0] + self.camera[0]) // self.tilemap.tile_size, int(mpos[1] + self.camera[1]) // self.tilemap.tile_size)

            if self.ongrid:
                self.screen.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.camera[0], tile_pos[1] * self.tilemap.tile_size - self.camera[1]))
            else:
                self.screen.blit(current_tile_img, mpos)


            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {
                    'type': self.tile_list[self.tile_group],
                    'variant': self.tile_variant,
                    'pos': tile_pos
                }
            if self.right_click:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.camera[0], tile['pos'][1] - self.camera[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.screen.blit(current_tile_img, (5, 5))

            # Atualiza e renderiza o background
            #self.background.update(self.camera)
            #self.background.render(self.display)


            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.camera[0], mpos[1] + self.camera[1])})
                    if event.button == 3:
                        self.right_click = True
                    if event.button == 4:  # Scroll Up
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            # Com Shift pressionado, muda a variante do tile
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        else:
                            # Sem Shift, muda o grupo de tiles
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0  # Reseta a variante ao mudar de grupo
                    if event.button == 5:  # Scroll Down
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            # Com Shift pressionado, muda a variante do tile
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                        else:
                            # Sem Shift, muda o grupo de tiles
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0  # Reseta a variante ao mudar de grupo
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_click = False


                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movemento[0] = True
                    elif event.key == pygame.K_a:
                        self.movemento[1] = True
                    elif event.key == pygame.K_w:
                        self.movemento[2] = True
                    elif event.key == pygame.K_s:
                        self.movemento[3] = True
                    elif event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    elif event.key == pygame.K_k:
                        self.tilemap.save('data/mapas/map.json')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movemento[0] = False
                    elif event.key == pygame.K_a:
                        self.movemento[1] = False
                    elif event.key == pygame.K_w:
                        self.movemento[2] = False
                    elif event.key == pygame.K_s:
                        self.movemento[3] = False


            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    editor = Editor()
    editor.run()
