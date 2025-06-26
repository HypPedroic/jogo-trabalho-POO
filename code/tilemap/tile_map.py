# Importando as bibliotecas necessárias
import pygame
import json
from utils.utils import load_images



class TileMap:
    def __init__(self, tile_size=16):
        self.__tile_size = tile_size
        self.__tilemap = {}
        self.__offgrid_tiles = []
        self.__NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (1, 1), (0, 1), (-1, 1)]
        self.__FISICA_ATIVADA = {'grass', 'stone'}
        self.__mapa_min_y = 0
        self.__limite_mapa_y = 1000  # Limite inicial do mapa
        
        # Carregando os assets do tilemap
        self.__assets = {
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
        return self.__tile_size
    
    @tile_size.setter
    def tile_size(self, value):
        self.__tile_size = value

    @property
    def tilemap(self):
        return self.__tilemap
    
    @tilemap.setter
    def tilemap(self, value):
        self.__tilemap = value

    @property
    def offgrid_tiles(self):
        return self.__offgrid_tiles
    
    @offgrid_tiles.setter
    def offgrid_tiles(self, value):
        self.__offgrid_tiles = value

    @property
    def NEIGHBOR_OFFSET(self):
        return self.__NEIGHBOR_OFFSET
    
    @NEIGHBOR_OFFSET.setter
    def NEIGHBOR_OFFSET(self, value):
        self.__NEIGHBOR_OFFSET = value
    
    @property
    def FISICA_ATIVADA(self):
        return self.__FISICA_ATIVADA
    
    @FISICA_ATIVADA.setter
    def FISICA_ATIVADA(self, value):
        self.__FISICA_ATIVADA = value
        
    @property
    def mapa_min_y(self):
        return self.__mapa_min_y
    
    @mapa_min_y.setter
    def mapa_min_y(self, value):
        self.__mapa_min_y = value
        
    @property
    def limite_mapa_y(self):
        return self.__limite_mapa_y
    
    @limite_mapa_y.setter
    def limite_mapa_y(self, value):
        self.__limite_mapa_y = value

    # Método para pegar os tiles ao redor de uma posição
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.__tile_size), int(pos[1] // self.__tile_size))
        for offset in self.__NEIGHBOR_OFFSET:
            check_lock = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_lock in self.__tilemap:
                tiles.append(self.__tilemap[check_lock])
        return tiles
    
    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'tilemap': self.__tilemap, 'tile_size': self.__tile_size, 'offgrid': self.__offgrid_tiles}, f)

    def load(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
            self.__tilemap = data['tilemap']
            self.__tile_size = data['tile_size']
            self.__offgrid_tiles = data['offgrid']
            
        self.__calcular_limite_mapa()

    # Método para pegar os retângulos ao redor de uma posição
    def fisica_rect_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in self.__FISICA_ATIVADA:
                rects.append(pygame.Rect(tile['pos'][0] * self.__tile_size, tile['pos'][1] * self.__tile_size, self.__tile_size, self.__tile_size))
        return rects

    # Definindo o método de renderização
    def renderizar(self, surf, offset=(0, 0)):
        for tile in self.__offgrid_tiles:
            surf.blit(self.__assets[tile['type']][tile['variant']], 
                     (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.__tile_size, (offset[0] + surf.get_width()) // self.__tile_size + 1):
            for y in range(offset[1] // self.__tile_size, (offset[1] + surf.get_height()) // self.__tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.__tilemap:
                    tile = self.__tilemap[loc]
                    surf.blit(self.__assets[tile['type']][tile['variant']], 
                             (tile['pos'][0] * self.__tile_size - offset[0], 
                              tile['pos'][1] * self.__tile_size - offset[1]))


    def procurar_objeto(self, id_pairs, keep=False):
        
        matches = []
        # Procura nos tiles offgrid
        for tile in self.offgrid_tiles:
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
        
        # Procura nos tiles do tilemap
        for loc in list(self.tilemap.keys()):  # <-- Faz uma cópia das chaves
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        

        return matches
    
    def __calcular_limite_mapa(self):
        if self and hasattr(self, "tilemap"):
            max_y = 0
            for pos_str in self.tilemap:
                if isinstance(pos_str, str):
                    pos_clean = pos_str.strip("()")
                    coords = pos_clean.split(";" if ";" in pos_clean else ", ")
                    pos = (int(coords[0]), int(coords[1]))
                else:
                    pos = pos_str

                if pos[1] > max_y:
                    max_y = pos[1]
            self.mapa_min_y = (max_y + 1) * self.tile_size
            self.limite_mapa_y = self.mapa_min_y + 500
        else:
            self.limite_mapa_y = 1000
                    
