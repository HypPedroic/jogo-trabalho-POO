import pygame
from utils.utils import load_image

class Background:
    def __init__(self, game):
        self.game = game
        self.layers = []
        
    def add_layer(self, image_path, scroll_speed):
        """
        Adiciona uma nova camada ao background
        :param image_path: Caminho da imagem da camada
        :param scroll_speed: Velocidade de rolagem (1.0 = velocidade normal, 0.5 = metade da velocidade, etc)
        """
        image = load_image(image_path)
        self.layers.append({
            'image': image,
            'scroll_speed': scroll_speed,
            'position': [0, 0]
        })
    
    def update(self, camera_pos):
        """
        Atualiza a posição das camadas baseado na posição da câmera
        """
        for layer in self.layers:
            # Atualiza a posição da camada baseado na velocidade de scroll
            layer['position'][0] = -camera_pos[0] * layer['scroll_speed']
            layer['position'][1] = -camera_pos[1] * layer['scroll_speed']
    
    def render(self, surface):
        """
        Renderiza todas as camadas do background
        """
        for layer in self.layers:
            # Calcula quantas vezes precisamos repetir a imagem horizontalmente
            image_width = layer['image'].get_width()
            image_height = layer['image'].get_height()
            screen_width = surface.get_width()
            screen_height = surface.get_height()
            
            # Calcula as posições inicial e final para renderização
            start_x = int(layer['position'][0] % image_width)
            start_y = int(layer['position'][1] % image_height)
            
            # Renderiza as imagens necessárias para cobrir a tela
            for x in range(start_x - image_width, screen_width, image_width):
                for y in range(start_y - image_height, screen_height, image_height):
                    surface.blit(layer['image'], (x, y)) 