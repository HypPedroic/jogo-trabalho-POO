from .backgroundlayer import BackgroundLayer
import json

class Background:
    def __init__(self, screen_height):
        self.__screen_height = screen_height
        self.__layers = []
        
    @property
    def screen_height(self):
        return self.__screen_height

    @screen_height.setter
    def screen_height(self, value):
        self.__screen_height = value

    @property
    def layers(self):
        return self.__layers

    @layers.setter
    def layers(self, value):
        self.__layers = value
        
    def add_layer(self, image_path, scroll_speed):
        """
        Adiciona uma nova camada ao background
        :param image_path: Caminho da imagem da camada
        :param scroll_speed: Velocidade de rolagem (1.0 = velocidade normal, 0.5 = metade da velocidade, etc)
        """
        layer = BackgroundLayer(image_path, scroll_speed, self.screen_height)
        self.layers.append(layer)
        
    def update(self, camera_pos):
        """Atualiza a posição de todas as camadas"""
        for layer in self.layers:
            layer.update(camera_pos)
    
    def render(self, surface):
        """Renderiza todas as camadas do background"""
        for layer in self.layers:
            layer.render(surface)
            
    def save(self, filepath):
        """Salva a configuração do background em um arquivo JSON"""
        data = {
            'screen_height': self.screen_height,
            'layers': [layer.to_dict() for layer in self.layers]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
    @classmethod
    def load(cls, filepath):
        """Carrega um background a partir de um arquivo JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        background = cls(data['screen_height'])
        for layer_data in data['layers']:
            background.add_layer(layer_data['image_path'], layer_data['scroll_speed'])
            
        return background
    
    def resize(self, new_height):
        """Redimensiona todas as camadas para uma nova altura"""
        self.screen_height = new_height
        for layer in self.layers:
            layer.resize(new_height)