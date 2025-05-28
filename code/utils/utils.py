# Importando as bibliotecas necessárias
import os
import pygame

# Caminho base das imagens
BASE_IMG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'images')

# Função para carregar imagens
def load_image(path):
    img = pygame.image.load(os.path.join(BASE_IMG_PATH, path)).convert_alpha()
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(os.path.join(BASE_IMG_PATH, path))):
        img = load_image(path + '/' + img_name)
        images.append(img)
    return images
        
