import pygame
from utils.utils import load_image

class BackgroundLayer:
    def __init__(self, image_path, scroll_speed, target_height):
        self.__image = load_image(image_path)
        self.__scroll_speed = scroll_speed
        self.__position = [0, 0]
        self.__resize(target_height)
        self.__image_path = image_path  # Salvar o caminho para poder recarregar/salvar depois
        
    def __resize(self, target_height):
        """Redimensiona a imagem mantendo a proporção"""
        aspect_ratio = self.__image.get_width() / self.__image.get_height()
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
        self.__image = pygame.transform.scale(self.__image, (new_width, new_height))
        
    def resize(self, target_height):
        """Método público para redimensionar a imagem"""
        self.__resize(target_height)
        
    def update(self, camera_pos):
        """Atualiza a posição da camada baseado na posição da câmera"""
        self.__position[0] = -camera_pos[0] * self.__scroll_speed
        self.__position[1] = -camera_pos[1] * self.__scroll_speed
        
    def render(self, surface):
        """Renderiza a camada do background"""
        image_width = self.__image.get_width()
        screen_width = surface.get_width()
        
        # Calcula a posição x inicial
        start_x = int(self.__position[0] % image_width)
        
        # Renderiza as imagens necessárias para cobrir a tela horizontalmente
        for x in range(start_x - image_width, screen_width + image_width, image_width):
            surface.blit(self.__image, (x, self.__position[1]))

            
    def to_dict(self):
        """Converte a camada para um dicionário para salvar"""
        return {
            'image_path': self.__image_path,
            'scroll_speed': self.__scroll_speed
        }
    
    @classmethod
    def from_dict(cls, data, target_height):
        """Cria uma nova camada a partir de um dicionário"""
        return cls(data['image_path'], data['scroll_speed'], target_height)