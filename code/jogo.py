# Importanto as bibliotecas necessárias
import pygame
import sys


# Importando as classes necessárias
from entidades.player import Player
from tilemap.tile_map import TileMap
from background.background import Background
from ui.game_interface import GameInterface
from menu.menu_moderno import MenuModerno


# Classe do jogo
class Jogo:
    # Inicializando o jogo
    def __init__(self):
        print("Inicializando pygame...")
        pygame.init()
        print("Pygame inicializado!")
        self._screen = pygame.display.set_mode((832, 640))
        self._display = pygame.Surface((624, 480))
        pygame.display.set_caption("JOGO SEM NOME NO MOMENTO")
        self._clock = pygame.time.Clock()
        self._running = True
        self._camera = [0, 0]

        # Estados do jogo
        self._estado = "menu"  # menu, jogando, game_over
        self._nome_jogador = ""

        # Menu moderno
        self._menu = MenuModerno(self._screen)
        self._menu.callback_iniciar_jogo = self.iniciar_jogo

        # Componentes do jogo (inicializados quando necessário)
        self._player = None
        self._tilemap = None
        self._background = None
        self._game_interface = None

        # Sistema de limbo
        self._limite_mapa_y = 1000  # Distância abaixo do mapa onde o player morre
        self._mapa_min_y = 0  # Será calculado baseado no tilemap

    # Properties para atributos que precisam ser acessados externamente
    @property
    def screen(self):
        return self._screen

    @property
    def display(self):
        return self._display

    @property
    def clock(self):
        return self._clock

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    @property
    def camera(self):
        return self._camera

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    @property
    def nome_jogador(self):
        return self._nome_jogador

    @nome_jogador.setter
    def nome_jogador(self, value):
        self._nome_jogador = value

    @property
    def menu(self):
        return self._menu

    @property
    def player(self):
        return self._player

    @property
    def tilemap(self):
        return self._tilemap

    @property
    def background(self):
        return self._background

    @property
    def game_interface(self):
        return self._game_interface

    def iniciar_jogo(self, nome_jogador):
        """Inicia um novo jogo com o nome do jogador"""
        self.nome_jogador = nome_jogador
        self.inicializar_componentes_jogo()
        self.estado = "jogando"

    def inicializar_componentes_jogo(self):
        """Inicializa todos os componentes necessários para o jogo"""
        # Inicializa o player
        self._player = Player((0, 0), (20, 32))

        # Inicializa o tilemap
        self._tilemap = TileMap(32)
        try:
            self._tilemap.load("data/mapas/map.json")
            # Calcula o limite inferior do mapa
            self.calcular_limite_mapa()
        except FileNotFoundError:
            print("Mapa não encontrado, usando configuração padrão")
            self._mapa_min_y = 0

        # Inicializa o background
        self._background = Background(self._screen.get_height())
        try:
            self._background = Background.load("data/backgrounds/default.json")
        except FileNotFoundError:
            pass

        # Inicializa a interface do jogo
        self._game_interface = GameInterface(self)
        self._game_interface.reset_timer()

    def calcular_limite_mapa(self):
        """Calcula o limite inferior do mapa baseado nos tiles"""
        if self._tilemap and hasattr(self._tilemap, "tilemap"):
            max_y = 0
            for pos_str in self._tilemap.tilemap:
                # Converte a string da posição para tupla de inteiros
                if isinstance(pos_str, str):
                    # Remove parênteses e divide por vírgula ou ponto e vírgula
                    pos_clean = pos_str.strip("()")
                    if ";" in pos_clean:
                        coords = pos_clean.split(";")
                    else:
                        coords = pos_clean.split(", ")
                    pos = (int(coords[0]), int(coords[1]))
                else:
                    pos = pos_str

                if pos[1] > max_y:
                    max_y = pos[1]
            # Define o limite como 500 pixels abaixo do tile mais baixo
            self._mapa_min_y = (max_y + 1) * self._tilemap.tile_size
            self._limite_mapa_y = self._mapa_min_y + 500
        else:
            # Valor padrão se não houver tilemap
            self._limite_mapa_y = 1000

    def verificar_limbo(self):
        """Verifica se o player caiu no limbo"""
        if self._player and self._player.retangulo().y > self._limite_mapa_y:
            self.player_morreu()

    def player_morreu(self):
        """Chamado quando o player morre"""
        tempo_jogo = None
        if self._game_interface:
            tempo_atual = pygame.time.get_ticks()
            tempo_jogo = (tempo_atual - self._game_interface.start_time) // 1000

        self._estado = "game_over"
        self._menu.mostrar_game_over(tempo_jogo)

    def inicializar_jogo(self):
        """Método mantido para compatibilidade"""
        self._estado = "jogando"

    def rodar_jogo(self):
        # Verifica se os componentes estão inicializados
        if (
            not self._player
            or not self._tilemap
            or not self._background
            or not self._game_interface
        ):
            return

        self._display.fill((52, 222, 235))

        self._camera[0] += (
            self._player.retangulo().centerx
            - self._display.get_width() / 2
            - self._camera[0]
        ) / 16
        self._camera[1] += (
            self._player.retangulo().centery
            - self._display.get_height() / 2
            - self._camera[1]
        ) / 16
        camera_movement = (int(self._camera[0]), int(self._camera[1]))

        # Atualiza e renderiza o background
        self._background.update(self._camera)
        self._background.render(self._display)

        self._tilemap.renderizar(self._display, offset=camera_movement)

        self._player.update(self._tilemap)
        self._player.renderizar(self._display, offset=camera_movement)

        # Verifica se o player caiu no limbo
        self.verificar_limbo()

        # Verifica se o player morreu (vida zero)
        if self._player.vida <= 0:
            self.player_morreu()
            return

        # Renderiza a interface do jogo
        self._game_interface.render(self._display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.constants.QUIT:
                self._running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self._player.mover_direita(True)
                elif event.key == pygame.K_LEFT:
                    self._player.mover_esquerda(True)
                if event.key == pygame.K_UP:
                    self._player.pular()
                if event.key == pygame.K_q:
                    self._player.alterar_estado()
                # Tecla ESC para voltar ao menu
                if event.key == pygame.K_ESCAPE:
                    self._estado = "menu"
                    self._menu.voltar_menu_principal()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self._player.mover_direita(False)
                elif event.key == pygame.K_LEFT:
                    self._player.mover_esquerda(False)

        self._screen.blit(
            pygame.transform.scale(self._display, self._screen.get_size()), (0, 0)
        )
        pygame.display.flip()
        self._clock.tick(60)

    def run(self):
        try:
            while self._running:
                if self._estado == "menu":
                    print("Executando menu...")
                    # Executa o menu e verifica se deve continuar
                    self._menu.running = True
                    nome = self._menu.run()
                    print(f"Menu retornou: {nome}")
                    if nome:  # Se retornou um nome, inicia o jogo
                        print(f"Iniciando jogo com jogador: {nome}")
                        self.iniciar_jogo(nome)
                    elif not self._menu.running:  # Se o menu foi fechado
                        print("Menu foi fechado, encerrando jogo")
                        self._running = False
                    else:
                        print("Menu continua rodando...")
                elif self._estado == "jogando":
                    self.rodar_jogo()
                elif self._estado == "game_over":
                    print("Executando menu de game over...")
                    # Executa o menu de game over
                    self._menu.running = True
                    self._menu.run()
                    if not self._menu.running:  # Se o menu foi fechado
                        print("Menu de game over foi fechado")
                        # Verifica se deve voltar ao menu principal ou sair
                        if self._menu.estado == "menu_principal":
                            self._estado = "menu"
                            print("Voltando ao menu principal")
                        else:
                            self._running = False
        except Exception as e:
            print(f"Erro durante execução do jogo: {e}")
            import traceback

            traceback.print_exc()
        finally:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    print("Iniciando o jogo...")
    try:
        jogo = Jogo()
        print("Jogo criado com sucesso!")
        print(f"Estado inicial: {jogo.estado}")
        jogo.run()
        print("Jogo finalizado.")
    except Exception as e:
        print(f"Erro ao inicializar o jogo: {e}")
        import traceback

        traceback.print_exc()
