import pygame
from entidades.player import Player
from .spawn_manager import SpawnManager
from tilemap.tile_map import TileMap
from background.background import Background
from ui.game_interface import GameInterface
from menu.menu import Menu
from particles.particles import Particle
import random
import os, json
import sys

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

        # Listas de entidades
        self.__projeteis = []
        self.__inimigos = []
        self.__particulas = []

        # Sistema de áudio
        self.__carregar_sistema_audio()
        
    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, value):
        self.__screen = value

    @property
    def display(self):
        return self.__display

    @display.setter
    def display(self, value):
        self.__display = value

    @property
    def clock(self):
        return self.__clock

    @clock.setter
    def clock(self, value):
        self.__clock = value

    @property
    def camera(self):
        return self.__camera

    @camera.setter
    def camera(self, value):
        self.__camera = value

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, value):
        self.__running = value

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value):
        self.__estado = value

    @property
    def nome_jogador(self):
        return self.__nome_jogador

    @nome_jogador.setter
    def nome_jogador(self, value):
        self.__nome_jogador = value

    @property
    def dificuldade(self):
        return self.__dificuldade

    @dificuldade.setter
    def dificuldade(self, value):
        self.__dificuldade = value

    @property
    def num_inimigos(self):
        return self.__num_inimigos

    @num_inimigos.setter
    def num_inimigos(self, value):
        self.__num_inimigos = value

    @property
    def menu(self):
        return self.__menu

    @menu.setter
    def menu(self, value):
        self.__menu = value

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        self.__player = value

    @property
    def tilemap(self):
        return self.__tilemap

    @tilemap.setter
    def tilemap(self, value):
        self.__tilemap = value

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, value):
        self.__background = value

    @property
    def game_interface(self):
        return self.__game_interface

    @game_interface.setter
    def game_interface(self, value):
        self.__game_interface = value

    @property
    def spawn_manager(self):
        return self.__spawn_manager

    @spawn_manager.setter
    def spawn_manager(self, value):
        self.__spawn_manager = value

    @property
    def projeteis(self):
        return self.__projeteis

    @projeteis.setter
    def projeteis(self, value):
        self.__projeteis = value

    @property
    def inimigos(self):
        return self.__inimigos

    @inimigos.setter
    def inimigos(self, value):
        self.__inimigos = value

    @property
    def particulas(self):
        return self.__particulas

    @particulas.setter
    def particulas(self, value):
        self.__particulas = value

    @property
    def musicas(self):
        return self.__musicas

    @musicas.setter
    def musicas(self, value):
        self.__musicas = value

    @property
    def sons(self):
        return self.__sons

    @sons.setter
    def sons(self, value):
        self.__sons = value

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
        self.nome_jogador = dados_jogo["nome"]
        self.dificuldade = dados_jogo["dificuldade"]
        self.num_inimigos = dados_jogo["num_inimigos"]
        self.__inicializar_componentes_jogo()
        self.estado = "jogando"

    def __inicializar_componentes_jogo(self):
        self.player = Player([0, 0], (20, 32))
        self.tilemap = TileMap(32)
        self.background = Background(self.__screen.get_height())
        self.game_interface = GameInterface(self)
        self.game_interface.reset_timer()
        
        try:
            self.tilemap.load("data/mapas/map1.json")
        except:
            pass
            
        for spawner in self.__tilemap.procurar_objeto([('Spawners', 0)]):

            print(spawner["pos"])
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']


        try:
            self.background = Background.load("data/backgrounds/default.json")
        except FileNotFoundError:
            pass
        
        

        self.spawn_manager = SpawnManager(self.tilemap, self.player, self.num_inimigos, game=self)
        self.spawn_manager.spawn_todos_inimigos()
        self.__tocar_musica_aleatoria()

    def __player_morreu(self):
        tempo_jogo = None
        if self.game_interface:
            tempo_atual = pygame.time.get_ticks()
            tempo_jogo = (tempo_atual - self.game_interface._GameInterface__start_time) // 1000
        self.__remover_progresso()  # Remove o save ao dar game over, se for do mesmo jogador
        self.estado = "game_over"
        self.menu.mostrar_game_over(tempo_jogo)
        pygame.mixer.music.stop()

    def __player_venceu(self):
        tempo_jogo = None
        if self.game_interface:
            tempo_atual = pygame.time.get_ticks()
            tempo_jogo = (tempo_atual - self.game_interface._GameInterface__start_time) // 1000
        pygame.mixer.music.stop()
        estatisticas = {
            "tempo": tempo_jogo,
            "inimigos_mortos": self.spawn_manager.get_inimigos_mortos() if self.spawn_manager else 0,
            "total_inimigos": self.spawn_manager.get_total_inimigos() if self.spawn_manager else 0,
            "vida_restante": self.player.vida if self.player else 0,
            "vida_maxima": self.player.vidaMax if self.player else 0,
        }
        self.__remover_progresso()  # Remove o save ao vencer, se for do mesmo jogador
        self.estado = "vitoria"
        if hasattr(self.menu, "mostrar_vitoria"):
            self.menu.mostrar_vitoria(tempo_jogo, estatisticas)

    def update(self):
        if self.estado == "jogando":
            self.__update_jogo()

    def __update_jogo(self):
        
        if not all([self.player, self.tilemap, self.background, self.game_interface]):
            return

        self.display.fill((52, 222, 235))

        self.__atualizar_camera()
        camera_movement = (int(self.camera[0]), int(self.camera[1]))

        self.background.update(self.camera)
        self.background.render(self.display)

        self.tilemap.renderizar(self.display, offset=camera_movement)

        self.player.update(self.tilemap, self)
        self.player.renderizar(self.display, offset=camera_movement)

        if self.spawn_manager:
            self.spawn_manager.update()
            self.spawn_manager.render(self.display, camera_movement)
            self.spawn_manager.verificar_colisoes_projeteis(self.projeteis)

        self.__atualizar_projeteis(camera_movement)
        self.__atualizar_Particulas(camera_movement)
        self.__verificar_estado_jogo()

        self.game_interface.render(self.display)

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
        )

    def __atualizar_camera(self):
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

    def __atualizar_projeteis(self, camera_movement):
        for projetil in self.projeteis:
            projetil.update(self, self.tilemap)
            projetil.renderizar(self.display, offset=camera_movement)
            if projetil.vida <= 0:
                self.projeteis.remove(projetil)
                
    def __atualizar_Particulas(self, camera_movement):
        for particula in self.particulas.copy():
            kill = particula.update()
            particula.render(self.display, offset=camera_movement)
            if kill:
                self.particulas.remove(particula)

    def __verificar_estado_jogo(self):
        if self.player.vida <= 0:
            self.__player_morreu()
        elif self.spawn_manager and self.spawn_manager.get_inimigos_vivos() == 0:
            self.__player_venceu()

    def __salvar_progresso(self):
        if not self.player:
            return False
        # Salvar inimigos vivos (posição e estado)
        inimigos_vivos = []
        if self.spawn_manager:
            for inimigo in self.spawn_manager._SpawnManager__inimigos_ativos:
                if hasattr(inimigo, 'pos') and getattr(inimigo, 'estado', None) != 'morto':
                    inimigo_data = {
                        'pos': list(inimigo.pos),
                        'tipo': type(inimigo).__name__,
                        'vida': getattr(inimigo, 'vida', 1),
                        'estado': getattr(inimigo, 'estado', 'idle')
                    }
                    # Adicionar propriedades específicas dos esqueletos
                    if type(inimigo).__name__ == 'Esqueleto':
                        inimigo_data['vida_maxima'] = getattr(inimigo, 'vida_maxima', 2)
                    inimigos_vivos.append(inimigo_data)
        progresso = {
            "nome": self.nome_jogador,
            "dificuldade": self.dificuldade,
            "num_inimigos": self.num_inimigos,
            "player": {
                "pos": list(self.player.pos),
                "vida": self.player.vida,
                "vidaMax": self.player.vidaMax,
                "furia": self.player.furia,
                "estado": self.player.estado,
                "pulos_disponiveis": self.player.pulos_disponiveis,
            },
            "tempo": self.game_interface.get_tempo() if self.game_interface else 0,
            "inimigos_vivos": self.spawn_manager.get_inimigos_vivos() if self.spawn_manager else 0,
            "inimigos_mortos": self.spawn_manager.get_inimigos_mortos() if self.spawn_manager else 0,
            "inimigos_totais": self.spawn_manager.get_total_inimigos() if self.spawn_manager else 0,
            "inimigos_ativos": inimigos_vivos
        }
        import os, json
        os.makedirs("data", exist_ok=True)
        with open("data/save.json", "w", encoding="utf-8") as f:
            json.dump(progresso, f, indent=2)
        return True

    def __carregar_progresso(self):
        import os, json
        save_path = "data/save.json"
        if not os.path.exists(save_path):
            return None
        with open(save_path, "r", encoding="utf-8") as f:
            progresso = json.load(f)
        return progresso

    def __remover_progresso(self):
        import os, json
        save_path = "data/save.json"
        if os.path.exists(save_path):
            try:
                with open(save_path, "r", encoding="utf-8") as f:
                    progresso = json.load(f)
                if progresso.get("nome") == self.nome_jogador:
                    os.remove(save_path)
            except Exception:
                pass

    def iniciar_jogo_carregado(self):
        progresso = self.__carregar_progresso()
        if not progresso:
            return
        self.nome_jogador = progresso["nome"]
        self.dificuldade = progresso["dificuldade"]
        self.num_inimigos = progresso["num_inimigos"]
        self.__inicializar_componentes_jogo()
        # Restaurar player
        p = progresso["player"]
        self.player.pos = p["pos"]
        self.player.vida = p["vida"]
        self.player.vidaMax = p["vidaMax"]
        self.player.furia = p["furia"]
        self.player.estado = p["estado"]
        self.player.pulos_disponiveis = p["pulos_disponiveis"]
        # Restaurar tempo
        if self.game_interface:
            self.game_interface.set_tempo(progresso.get("tempo", 0))
        # Restaurar inimigos ativos
        if self.spawn_manager:
            self.spawn_manager._SpawnManager__inimigos_ativos.clear()
            for inimigo_data in progresso.get("inimigos_ativos", []):
                if inimigo_data['tipo'] == 'Slime':
                    from entidades.slime import Slime
                    inimigo = Slime(tuple(inimigo_data['pos']), (16, 16))
                    # Restaurar propriedades do slime
                    inimigo.vida = inimigo_data.get('vida', 1)
                    inimigo.estado = inimigo_data.get('estado', 'idle')
                    self.spawn_manager._SpawnManager__inimigos_ativos.append(inimigo)
                elif inimigo_data['tipo'] == 'Esqueleto':
                    from entidades.esqueleto import Esqueleto
                    inimigo = Esqueleto(tuple(inimigo_data['pos']), (32, 32), game=self)
                    # Restaurar propriedades do esqueleto
                    inimigo.vida = inimigo_data.get('vida', 2)
                    inimigo.vida_maxima = inimigo_data.get('vida_maxima', 2)
                    inimigo.estado = inimigo_data.get('estado', 'inativo')
                    self.spawn_manager._SpawnManager__inimigos_ativos.append(inimigo)
            self.spawn_manager._SpawnManager__inimigos_mortos = progresso.get("inimigos_mortos", 0)
            self.spawn_manager._SpawnManager__max_inimigos = len(progresso.get("inimigos_ativos", []))
            self.spawn_manager._SpawnManager__inimigos_totais = progresso.get("inimigos_totais", self.__num_inimigos)
        self.estado = "jogando"

    def mostrar_menu_pausa(self):
        largura, altura = self.screen.get_size()
        fonte = pygame.font.SysFont("Arial", 32, bold=True)
        opcoes = ["Salvar", "Sair", "Voltar"]
        selecionado = 0
        rodando = True
        mensagem = ""
        tempo_pausado = 0
        if self.game_interface:
            tempo_pausado = self.game_interface.get_tempo()
        while rodando:
            self.screen.fill((25, 25, 35))
            titulo = fonte.render("PAUSADO", True, (64, 224, 208))
            self.screen.blit(titulo, (largura // 2 - titulo.get_width() // 2, 120))
            for i, texto in enumerate(opcoes):
                cor = (255, 99, 71) if i == selecionado else (240, 240, 240)
                botao = fonte.render(texto, True, cor)
                self.screen.blit(botao, (largura // 2 - botao.get_width() // 2, 220 + i * 70))
            if mensagem:
                msg_surf = fonte.render(mensagem, True, (0,255,0))
                self.screen.blit(msg_surf, (largura // 2 - msg_surf.get_width() // 2, 450))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "sair"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selecionado = (selecionado - 1) % len(opcoes)
                    elif event.key == pygame.K_DOWN:
                        selecionado = (selecionado + 1) % len(opcoes)
                    elif event.key == pygame.K_RETURN:
                        if opcoes[selecionado] == "Salvar":
                            if self.__salvar_progresso():
                                mensagem = "Jogo salvo com sucesso!"
                            else:
                                mensagem = "Erro ao salvar!"
                        elif opcoes[selecionado] == "Sair":
                            pygame.quit()
                            sys.exit()
                        elif opcoes[selecionado] == "Voltar":
                            rodando = False
                            mensagem = ""
                            # Retomar cronômetro
                            if self.game_interface:
                                self.game_interface.set_tempo(tempo_pausado)
                    elif event.key == pygame.K_ESCAPE:
                        rodando = False
                        mensagem = ""
                        if self.game_interface:
                            self.game_interface.set_tempo(tempo_pausado)
        return None

    def processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.estado == "jogando" and event.key == pygame.K_ESCAPE:
                    acao = self.mostrar_menu_pausa()
                    if acao == "sair":
                        self.estado = "menu"
                        self.menu.voltar_menu_principal()
                else:
                    self.__processar_input_teclado(event.key, True)
            elif event.type == pygame.KEYUP:
                self.__processar_input_teclado(event.key, False)

    def __processar_input_teclado(self, key, pressed):
        if self.estado == "jogando":
            if pressed:
                if key == pygame.K_RIGHT:
                    self.player.mover_direita(True)
                elif key == pygame.K_LEFT:
                    self.player.mover_esquerda(True)
                elif key == pygame.K_UP:
                    self.player.pular()
                elif key == pygame.K_q:
                    self.player.ativar_furia(self)
                elif key == pygame.K_SPACE:
                    self.player.atacar()
                elif key == pygame.K_ESCAPE:
                    self.estado = "menu"
                    self.menu.voltar_menu_principal()
                elif key == pygame.K_p:
                    self.__toggle_pausar_musica()
                elif key == pygame.K_PLUS or key == pygame.K_KP_PLUS:
                    self.__ajustar_volume_musica(0.1)
                elif key == pygame.K_MINUS or key == pygame.K_KP_MINUS:
                    self.__ajustar_volume_musica(-0.1)
            else:
                if key == pygame.K_RIGHT:
                    self.player.mover_direita(False)
                elif key == pygame.K_LEFT:
                    self.player.mover_esquerda(False)

    def __toggle_pausar_musica(self):
        if pygame.mixer.music.get_busy():
            if pygame.mixer.music.get_pos() != -1:
                if pygame.mixer.music.get_volume() > 0:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.unpause()

    def __ajustar_volume_musica(self, delta):
        vol = pygame.mixer.music.get_volume()
        novo_vol = max(0.0, min(1.0, vol + delta))
        pygame.mixer.music.set_volume(novo_vol)
        print(f"Volume da música: {int(novo_vol*100)}%")
