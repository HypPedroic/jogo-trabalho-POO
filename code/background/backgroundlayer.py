import pygame
from utils.utils import load_image

class BackgroundLayer:
    def __init__(self, image_path, scroll_speed, target_height):
        self.image = load_image(image_path)
        self.scroll_speed = scroll_speed
        self.position = [0, 0]
        self.resize(target_height)
        self.image_path = image_path  # Salvar o caminho para poder recarregar/salvar depois
        
    def resize(self, target_height):
        """Redimensiona a imagem mantendo a proporção"""
        aspect_ratio = self.image.get_width() / self.image.get_height()
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
    def update(self, camera_pos):
        """Atualiza a posição da camada baseado na posição da câmera"""
        self.position[0] = -camera_pos[0] * self.scroll_speed
        self.position[1] = -camera_pos[1] * self.scroll_speed
        
    def render(self, surface):
        """Renderiza a camada do background"""
        image_width = self.image.get_width()
        screen_width = surface.get_width()
        
        # Calcula a posição x inicial
        start_x = int(self.position[0] % image_width)
        
        # Renderiza as imagens necessárias para cobrir a tela horizontalmente
        for x in range(start_x - image_width, screen_width + image_width, image_width):
            surface.blit(self.image, (x, self.position[1]))

            
    def to_dict(self):
        """Converte a camada para um dicionário para salvar"""
        return {
            'image_path': self.image_path,
            'scroll_speed': self.scroll_speed
        }
    
    @classmethod
    def from_dict(cls, data, target_height):
        """Cria uma nova camada a partir de um dicionário"""
        return cls(data['image_path'], data['scroll_speed'], target_height)