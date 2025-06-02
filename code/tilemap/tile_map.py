# Importando as bibliotecas necessárias
import pygame
import json
from utils.utils import load_images


#OFFSET DOS VIZINHOS
NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (1, 1), (0, 1), (-1, 1)]
FISICA_ATIVADA = {'grass', 'stone'}

class TileMap:
    def __init__(self, tile_size=16):
        self._tile_size = tile_size
        self._tilemap = {}
        self._offgrid_tiles = []
        
        # Carregando os assets do tilemap
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
        }

    @property
    def tile_size(self):
        return self._tile_size
    
    @tile_size.setter
    def tile_size(self, value):
        self._tile_size = value

    @property
    def tilemap(self):
        return self._tilemap
    
    @tilemap.setter
    def tilemap(self, value):
        self._tilemap = value

    @property
    def offgrid_tiles(self):
        return self._offgrid_tiles
    
    @offgrid_tiles.setter
    def offgrid_tiles(self, value):
        self._offgrid_tiles = value

    # Método para pegar os tiles ao redor de uma posição
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_lock = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_lock in self._tilemap:
                tiles.append(self._tilemap[check_lock])
        return tiles
    
    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)

    def load(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
            self.tilemap = data['tilemap']
            self.tile_size = data['tile_size']
            self.offgrid_tiles = data['offgrid']

    # Método para pegar os retângulos ao redor de uma posição
    def fisica_rect_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in FISICA_ATIVADA:
                rects.append(pygame.Rect(tile['pos'][0] * self._tile_size, tile['pos'][1] * self._tile_size, self._tile_size, self._tile_size))
        return rects

    # Definindo o método de renderização
    def renderizar(self, surf, offset=(0, 0)):
        for tile in self._offgrid_tiles:
            surf.blit(self.assets[tile['type']][tile['variant']], 
                     (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # Renderiza os tiles fora da grade, por isso não é necessário multiplicar pelo tamanho do tile
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.assets[tile['type']][tile['variant']], 
                             (tile['pos'][0] * self._tile_size - offset[0], 
                              tile['pos'][1] * self._tile_size - offset[1]))
                    
        

        

       
