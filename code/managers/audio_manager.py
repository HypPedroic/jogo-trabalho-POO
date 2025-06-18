import pygame
import random

class AudioManager:
    def __init__(self):
        self.__musicas = [
            "01 Blossom Tree.wav",
            "03 Himawari No Sato.wav",
            "04 Whispering Stars.wav",
            "06 Tengu.wav",
            "07 Gion District.wav",
            "08 Higanbana Field.wav",
        ]
        self.__sons = {}
        self.__carregar_sons()

    def __carregar_sons(self):
        """Carrega todos os efeitos sonoros"""
        try:
            self.__sons["tiro"] = pygame.mixer.Sound("data/sounds/sound-tiro.wav")
            self.__sons["ataque"] = pygame.mixer.Sound("data/sounds/sound-ataque.wav")
            self.__sons["dano"] = pygame.mixer.Sound("data/sounds/sound-tomando-dano.wav")
            self.__sons["matando_inimigo"] = pygame.mixer.Sound("data/sounds/sound-matando-inimigo.wav")
            self.__sons["furia"] = pygame.mixer.Sound("data/sounds/sound-puxando-foice-furia.wav")
        except pygame.error as e:
            print(f"Erro ao carregar sons: {e}")

    def tocar_som(self, nome_som):
        """Toca um efeito sonoro específico"""
        if nome_som in self.__sons:
            try:
                self.__sons[nome_som].play()
            except pygame.error as e:
                print(f"Erro ao tocar som {nome_som}: {e}")

    def tocar_musica_aleatoria(self):
        """Toca uma música de fundo aleatória"""
        try:
            musica_escolhida = random.choice(self.__musicas)
            caminho_musica = f"data/music/{musica_escolhida}"
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            print(f"Tocando música: {musica_escolhida}")
        except pygame.error as e:
            print(f"Erro ao carregar música: {e}")

    def parar_musica(self):
        """Para a música atual"""
        pygame.mixer.music.stop()

    def pausar_musica(self):
        """Pausa a música atual"""
        pygame.mixer.music.pause()

    def despausar_musica(self):
        """Despausa a música atual"""
        pygame.mixer.music.unpause()

    def ajustar_volume_musica(self, volume):
        """Ajusta o volume da música (0.0 a 1.0)"""
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))

    def ajustar_volume_som(self, nome_som, volume):
        """Ajusta o volume de um efeito sonoro específico (0.0 a 1.0)"""
        if nome_som in self.__sons:
            self.__sons[nome_som].set_volume(max(0.0, min(1.0, volume)))