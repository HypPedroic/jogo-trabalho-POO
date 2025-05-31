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
        # Carrega a imagem original
        image = load_image(image_path)
        
        # Obtém as dimensões da tela
        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()
        
        # Redimensiona a imagem para corresponder à altura da tela e manter a proporção
        aspect_ratio = image.get_width() / image.get_height()
        new_height = screen_height
        new_width = int(new_height * aspect_ratio)
        
        # Redimensiona a imagem
        image = pygame.transform.scale(image, (new_width, new_height))
        
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
            # Obtém as dimensões
            image_width = layer['image'].get_width()
            screen_width = surface.get_width()
            
            # Calcula a posição x inicial
            start_x = int(layer['position'][0] % image_width)
            
            # Renderiza as imagens necessárias para cobrir a tela horizontalmente
            for x in range(start_x - image_width, screen_width + image_width, image_width):
                # Renderiza a imagem apenas uma vez na vertical
                surface.blit(layer['image'], (x, layer['position'][1])) 