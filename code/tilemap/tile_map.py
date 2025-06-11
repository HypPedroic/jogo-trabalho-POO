# Importando as bibliotecas necessárias
import pygame
import json
from utils.utils import load_images



class TileMap:
    def __init__(self, tile_size=16):
        self._tile_size = tile_size
        self._tilemap = {}
        self._offgrid_tiles = []
        self._NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (1, 1), (0, 1), (-1, 1)]
        self._FISICA_ATIVADA = {'grass', 'stone'}
        
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
            'Spawners': load_images('Objetos/spawners')
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

    @property
    def NEIGHBOR_OFFSET(self):
        return self._NEIGHBOR_OFFSET
    
    @NEIGHBOR_OFFSET.setter
    def NEIGHBOR_OFFSET(self, value):
        self._NEIGHBOR_OFFSET = value
    
    @property
    def FISICA_ATIVADA(self):
        return self._FISICA_ATIVADA
    
    @FISICA_ATIVADA.setter
    def FISICA_ATIVADA(self, value):
        self._FISICA_ATIVADA = value

    # Método para pegar os tiles ao redor de uma posição
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in self.NEIGHBOR_OFFSET:
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
            if tile['type'] in self.FISICA_ATIVADA:
                rects.append(pygame.Rect(tile['pos'][0] * self._tile_size, tile['pos'][1] * self._tile_size, self._tile_size, self._tile_size))
        return rects

    # Definindo o método de renderização
    def renderizar(self, surf, offset=(0, 0)):
        for tile in self._offgrid_tiles:
            surf.blit(self.assets[tile['type']][tile['variant']], 
                     (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.assets[tile['type']][tile['variant']], 
                             (tile['pos'][0] * self._tile_size - offset[0], 
                              tile['pos'][1] * self._tile_size - offset[1]))


    def procurar_objeto(self, tipo, variant, remover=False):
        """
        Procura o primeiro objeto do tipo e variante especificados no tilemap.
        Retorna a posição (x, y) do objeto encontrado.
        Se remover=True, remove o objeto do tilemap.
        """
        # Procura nos tiles do grid
        for loc, tile in list(self.tilemap.items()):
            if tile['type'] == tipo and tile['variant'] == variant:
                pos = (tile['pos'][0], tile['pos'][1])
                if remover:
                    del self.tilemap[loc]
                return pos

        # Procura nos offgrid_tiles
        for i, tile in enumerate(self.offgrid_tiles):
            if tile['type'] == tipo and tile['variant'] == variant:
                pos = (tile['pos'][0], tile['pos'][1])
                if remover:
                    self.offgrid_tiles.pop(i)
                return pos

        return None  # Não encontrado       
                    
        

        

       
