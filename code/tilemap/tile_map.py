# Importando as bibliotecas necessárias
import pygame

#OFFSET DOS VIZINHOS
NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (1, 1), (0, 1), (-1, 1)]
FISICA_ATIVADA = {'grass', 'stone'}

class TileMap:
    def __init__(self, game, tile_size=32):
        self._game = game
        self._tile_size = tile_size
        self._tilemap = {}
        self._offgrid_tiles = []

        for i in range(10):
            self._tilemap[str(0+i) + ';9'] = {'type': 'grass', 'variant': 1, 'pos': (0 + i, 9)}
            self._tilemap['10;' + str(0+i)] = {'type': 'grass', 'variant': 11, 'pos': (10, 0 + i)}

    # Definindo os getters e setters
    @property
    def game(self):
        return self._game
    
    @game.setter 
    def game(self, value):
        self._game = value

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
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # Renderiza os tiles fora da grade, por isso não é necessário multiplicar pelo tamanho do tile
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self._tile_size - offset[0], tile['pos'][1] * self._tile_size - offset[1]))
                    
        

        

       
