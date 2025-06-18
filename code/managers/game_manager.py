import pygame
from entidades.player import Player
from entidades.spawn_manager import SpawnManager
from tilemap.tile_map import TileMap
from background.background import Background
from ui.game_interface import GameInterface
from menu.menu import Menu
import random

class GameManager:
    def __init__(self, screen):
        self.__screen = screen
        self.__display = pygame.Surface((624, 480))
        self.__clock = pygame.time.Clock()
        self.__camera = [0, 0]
        self.__running = True
        self.__estado = "menu"
        self.__nome_jogador = ""
        self.__dificuldade = "NORMAL"
        self.__num_inimigos = 15

        # Componentes do jogo
        self.__menu = Menu(self.__screen)
        self.__menu.callback_iniciar_jogo = self.iniciar_jogo
        self.__player = None
        self.__tilemap = None
        self.__background = None
        self.__game_interface = None
        self.__spawn_manager = None

        # Sistema de limbo
        self.__limite_mapa_y = 1000
        self.__mapa_min_y = 0

        # Listas de entidades
        self.projeteis = []
        self.inimigos = []

        # Sistema de áudio
        self.__carregar_sistema_audio()

    def __carregar_sistema_audio(self):
        self.__musicas = [
            "01 Blossom Tree.wav",
            "03 Himawari No Sato.wav",
            "04 Whispering Stars.wav",
            "06 Tengu.wav",
            "07 Gion District.wav",
            "08 Higanbana Field.wav",
        ]
        self.__sons = {}
        try:
            self.__sons["tiro"] = pygame.mixer.Sound("data/sounds/sound-tiro.wav")
            self.__sons["ataque"] = pygame.mixer.Sound("data/sounds/sound-ataque.wav")
            self.__sons["dano"] = pygame.mixer.Sound("data/sounds/sound-tomando-dano.wav")
            self.__sons["matando_inimigo"] = pygame.mixer.Sound("data/sounds/sound-matando-inimigo.wav")
            self.__sons["furia"] = pygame.mixer.Sound("data/sounds/sound-puxando-foice-furia.wav")
        except pygame.error as e:
            print(f"Erro ao carregar sons: {e}")

    @property
    def player(self):
        return self.__player

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value):
        self.__estado = value

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, value):
        self.__running = value

    @property
    def menu(self):
        return self.__menu

    @property
    def clock(self):
        return self.__clock

    def tocar_som(self, nome_som):
        if nome_som in self.__sons:
            try:
                self.__sons[nome_som].play()
            except pygame.error as e:
                print(f"Erro ao tocar som {nome_som}: {e}")

    def __tocar_musica_aleatoria(self):
        try:
            musica_escolhida = random.choice(self.__musicas)
            caminho_musica = f"data/music/{musica_escolhida}"
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erro ao carregar música: {e}")

    def iniciar_jogo(self, dados_jogo):
        self.__nome_jogador = dados_jogo["nome"]
        self.__dificuldade = dados_jogo["dificuldade"]
        self.__num_inimigos = dados_jogo["num_inimigos"]
        self.__inicializar_componentes_jogo()
        self.__estado = "jogando"

    def __inicializar_componentes_jogo(self):
        self.__player = Player((0, 0), (20, 32))
        self.__tilemap = TileMap(32)
        self.__background = Background(self.__screen.get_height())
        self.__game_interface = GameInterface(self)
        self.__game_interface.reset_timer()

        try:
            self.__tilemap.load("data/mapas/map.json")
            self.__calcular_limite_mapa()
        except FileNotFoundError:
            print("Mapa não encontrado, usando configuração padrão")

        try:
            self.__background = Background.load("data/backgrounds/default.json")
        except FileNotFoundError:
            pass

        self.__spawn_manager = SpawnManager(self.__tilemap, self.__player, self.__num_inimigos)
        self.__spawn_manager.game = self
        self.__spawn_manager.spawn_todos_inimigos()
        self.__tocar_musica_aleatoria()

    def __calcular_limite_mapa(self):
        if self.__tilemap and hasattr(self.__tilemap, "tilemap"):
            max_y = 0
            for pos_str in self.__tilemap.tilemap:
                if isinstance(pos_str, str):
                    pos_clean = pos_str.strip("()")
                    coords = pos_clean.split(";" if ";" in pos_clean else ", ")
                    pos = (int(coords[0]), int(coords[1]))
                else:
                    pos = pos_str

                if pos[1] > max_y:
                    max_y = pos[1]
            self.__mapa_min_y = (max_y + 1) * self.__tilemap.tile_size
            self.__limite_mapa_y = self.__mapa_min_y + 500
        else:
            self.__limite_mapa_y = 1000

    def __verificar_limbo(self):
        if self.__player and self.__player.retangulo().y > self.__limite_mapa_y:
            self.__player_morreu()

    def __player_morreu(self):
        tempo_jogo = None
        if self.__game_interface:
            tempo_atual = pygame.time.get_ticks()
            tempo_jogo = (tempo_atual - self.__game_interface._GameInterface__start_time) // 1000

        self.__estado = "game_over"
        self.__menu.mostrar_game_over(tempo_jogo)
        pygame.mixer.music.stop()

    def __player_venceu(self):
        tempo_jogo = None
        if self.__game_interface:
            tempo_atual = pygame.time.get_ticks()
            tempo_jogo = (tempo_atual - self.__game_interface._GameInterface__start_time) // 1000

        pygame.mixer.music.stop()

        estatisticas = {
            "tempo": tempo_jogo,
            "inimigos_mortos": self.__spawn_manager.get_inimigos_mortos() if self.__spawn_manager else 0,
            "total_inimigos": self.__spawn_manager.get_total_inimigos() if self.__spawn_manager else 0,
            "vida_restante": self.__player.vida if self.__player else 0,
            "vida_maxima": self.__player.vidaMax if self.__player else 0,
        }

        self.__estado = "vitoria"
        if hasattr(self.__menu, "mostrar_vitoria"):
            self.__menu.mostrar_vitoria(tempo_jogo, estatisticas)

    def update(self):
        if self.__estado == "jogando":
            self.__update_jogo()

    def __update_jogo(self):
        if not all([self.__player, self.__tilemap, self.__background, self.__game_interface]):
            return

        self.__display.fill((52, 222, 235))

        self.__atualizar_camera()
        camera_movement = (int(self.__camera[0]), int(self.__camera[1]))

        self.__background.update(self.__camera)
        self.__background.render(self.__display)

        self.__tilemap.renderizar(self.__display, offset=camera_movement)

        self.__player.update(self.__tilemap, self)
        self.__player.renderizar(self.__display, offset=camera_movement)

        if self.__spawn_manager:
            self.__spawn_manager.update()
            self.__spawn_manager.render(self.__display, camera_movement)
            self.__spawn_manager.verificar_colisoes_projeteis(self.projeteis)

        self.__atualizar_projeteis(camera_movement)
        self.__verificar_limbo()
        self.__verificar_estado_jogo()

        self.__game_interface.render(self.__display)

        self.__screen.blit(
            pygame.transform.scale(self.__display, self.__screen.get_size()), (0, 0)
        )

    def __atualizar_camera(self):
        self.__camera[0] += (
            self.__player.retangulo().centerx
            - self.__display.get_width() / 2
            - self.__camera[0]
        ) / 16
        self.__camera[1] += (
            self.__player.retangulo().centery
            - self.__display.get_height() / 2
            - self.__camera[1]
        ) / 16

    def __atualizar_projeteis(self, camera_movement):
        for projetil in self.projeteis:
            projetil.update(self, self.__tilemap)
            projetil.renderizar(self.__display, offset=camera_movement)
            if projetil.vida <= 0:
                self.projeteis.remove(projetil)

    def __verificar_estado_jogo(self):
        if self.__player.vida <= 0:
            self.__player_morreu()
        elif self.__spawn_manager and self.__spawn_manager.get_inimigos_vivos() == 0:
            self.__player_venceu()

    def processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                self.__processar_input_teclado(event.key, True)
            elif event.type == pygame.KEYUP:
                self.__processar_input_teclado(event.key, False)

    def __processar_input_teclado(self, key, pressed):
        if self.__estado == "jogando":
            if pressed:
                if key == pygame.K_RIGHT:
                    self.__player.mover_direita(True)
                elif key == pygame.K_LEFT:
                    self.__player.mover_esquerda(True)
                elif key == pygame.K_UP:
                    self.__player.pular()
                elif key == pygame.K_q:
                    self.__player.ativar_furia(self)
                elif key == pygame.K_SPACE:
                    self.__player.atacar()
                elif key == pygame.K_ESCAPE:
                    self.__estado = "menu"
                    self.__menu.voltar_menu_principal()
            else:
                if key == pygame.K_RIGHT:
                    self.__player.mover_direita(False)
                elif key == pygame.K_LEFT:
                    self.__player.mover_esquerda(False)

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value):
        self.__estado = value

    @property
    def running(self):
        return self.__running

    @property
    def menu(self):
        return self.__menu

    @property
    def screen(self):
        return self.__screen

    @property
    def display(self):
        return self.__display

    @property
    def clock(self):
        return self.__clock