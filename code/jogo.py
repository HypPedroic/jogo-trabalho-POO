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
        self.screen = pygame.display.set_mode((832, 640))
        self.display = pygame.Surface((624, 480))
        pygame.display.set_caption("JOGO SEM NOME NO MOMENTO")
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera = [0, 0]

        # Estados do jogo
        self.estado = "menu"  # menu, jogando, game_over
        self.nome_jogador = ""

        # Menu moderno
        self.menu = MenuModerno(self.screen)
        self.menu.callback_iniciar_jogo = self.iniciar_jogo

        # Componentes do jogo (inicializados quando necessário)
        self.player = None
        self.tilemap = None
        self.background = None
        self.game_interface = None

        # Sistema de limbo
        self.limite_mapa_y = 1000  # Distância abaixo do mapa onde o player morre
        self.mapa_min_y = 0  # Será calculado baseado no tilemap

    def iniciar_jogo(self, nome_jogador):
        """Inicia um novo jogo com o nome do jogador"""
        self.nome_jogador = nome_jogador
        self.inicializar_componentes_jogo()
        self.estado = "jogando"

    def inicializar_componentes_jogo(self):
        """Inicializa todos os componentes necessários para o jogo"""
        # Inicializa o player
        self.player = Player((0, 0), (20, 32))

        # Inicializa o tilemap
        self.tilemap = TileMap(32)
        try:
            self.tilemap.load("data/mapas/map.json")
            # Calcula o limite inferior do mapa
            self.calcular_limite_mapa()
        except FileNotFoundError:
            print("Mapa não encontrado, usando configuração padrão")
            self.mapa_min_y = 0

        # Inicializa o background
        self.background = Background(self.screen.get_height())
        try:
            self.background = Background.load("data/backgrounds/default.json")
        except FileNotFoundError:
            pass

        # Inicializa a interface do jogo
        self.game_interface = GameInterface(self)
        self.game_interface.reset_timer()

    def calcular_limite_mapa(self):
        """Calcula o limite inferior do mapa baseado nos tiles"""
        if self.tilemap and hasattr(self.tilemap, "tilemap"):
            max_y = 0
            for pos_str in self.tilemap.tilemap:
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
            self.mapa_min_y = (max_y + 1) * self.tilemap.tile_size
            self.limite_mapa_y = self.mapa_min_y + 500
        else:
            self.mapa_min_y = 0
            self.limite_mapa_y = 1000

    def verificar_limbo(self):
        """Verifica se o player caiu no limbo"""
        if self.player and self.player.retangulo().y > self.limite_mapa_y:
            self.player_morreu()

    def player_morreu(self):
        """Chamado quando o player morre"""
        tempo_jogo = None
        if self.game_interface:
            tempo_atual = pygame.time.get_ticks()
            tempo_jogo = (tempo_atual - self.game_interface.start_time) // 1000

        self.estado = "game_over"
        self.menu.mostrar_game_over(tempo_jogo)

    def inicializar_jogo(self):
        """Método mantido para compatibilidade"""
        self.estado = "jogando"

    def rodar_jogo(self):
        # Verifica se os componentes estão inicializados
        if (
            not self.player
            or not self.tilemap
            or not self.background
            or not self.game_interface
        ):
            return

        self.display.fill((52, 222, 235))

        self.camera[0] += (
            self.player.retangulo().centerx
            - self.display.get_width() / 2
            - self.camera[0]
        ) / 16
        self.camera[1] += (
            self.player.retangulo().centery
            - self.display.get_height() / 2
            - self.camera[1]
        ) / 16
        camera_movement = (int(self.camera[0]), int(self.camera[1]))

        # Atualiza e renderiza o background
        self.background.update(self.camera)
        self.background.render(self.display)

        self.tilemap.renderizar(self.display, offset=camera_movement)

        self.player.update(self.tilemap)
        self.player.renderizar(self.display, offset=camera_movement)

        # Verifica se o player caiu no limbo
        self.verificar_limbo()

        # Verifica se o player morreu (vida zero)
        if self.player.vida <= 0:
            self.player_morreu()
            return

        # Renderiza a interface do jogo
        self.game_interface.render(self.display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.constants.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.mover_direita(True)
                elif event.key == pygame.K_LEFT:
                    self.player.mover_esquerda(True)
                if event.key == pygame.K_UP:
                    self.player.pular()
                if event.key == pygame.K_q:
                    self.player.alterar_estado()
                # Tecla ESC para voltar ao menu
                if event.key == pygame.K_ESCAPE:
                    self.estado = "menu"
                    self.menu.voltar_menu_principal()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.mover_direita(False)
                elif event.key == pygame.K_LEFT:
                    self.player.mover_esquerda(False)

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
        )
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        try:
            while self.running:
                if self.estado == "menu":
                    print("Executando menu...")
                    # Executa o menu e verifica se deve continuar
                    self.menu.running = True
                    nome = self.menu.run()
                    print(f"Menu retornou: {nome}")
                    if nome:  # Se retornou um nome, inicia o jogo
                        print(f"Iniciando jogo com jogador: {nome}")
                        self.iniciar_jogo(nome)
                    elif not self.menu.running:  # Se o menu foi fechado
                        print("Menu foi fechado, encerrando jogo")
                        self.running = False
                    else:
                        print("Menu continua rodando...")
                elif self.estado == "jogando":
                    self.rodar_jogo()
                elif self.estado == "game_over":
                    print("Executando menu de game over...")
                    # Executa o menu de game over
                    self.menu.running = True
                    self.menu.run()
                    if not self.menu.running:  # Se o menu foi fechado
                        print("Menu de game over foi fechado")
                        # Verifica se deve voltar ao menu principal ou sair
                        if self.menu.estado == "menu_principal":
                            self.estado = "menu"
                            print("Voltando ao menu principal")
                        else:
                            self.running = False
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
