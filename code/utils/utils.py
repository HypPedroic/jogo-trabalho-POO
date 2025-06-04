# Importando as bibliotecas necessárias
import os
import pygame


# Caminho base das imagens
BASE_IMG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "images"
)


# Função para carregar imagens
def load_image(path):
    img = pygame.image.load(os.path.join(BASE_IMG_PATH, path)).convert_alpha()
    return img


def load_images(path):
    images = []
    full_path = os.path.join(BASE_IMG_PATH, path)

    if not os.path.exists(full_path):
        print(f"Aviso: Pasta não encontrada: {full_path}")
        return images

    try:
        for img_name in sorted(os.listdir(full_path)):
            if img_name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                img = load_image(path + "/" + img_name)
                images.append(img)
    except Exception as e:
        print(f"Erro ao carregar imagens de {path}: {e}")

    return images
