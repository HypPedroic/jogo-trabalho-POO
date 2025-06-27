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

    @property
    def projeteis(self):
        return self.__projeteis
    
    @projeteis.setter
    def projeteis(self, value):
        self.__projeteis = value

    @property
    def inimigos(self):
        return self.__inimigos

    @property
    def particulas(self):
        return self.__particulas
    
    @property
    def display(self):
        return self.__display
    
    @display.setter
    def display(self, value):
        self.__display = value
<<<<<<< HEAD
    
    @property
    def spawn_manager(self):
        return self.__spawn_manager
=======
>>>>>>> main

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
        self.__player = Player([0, 0], (20, 32))
        self.__tilemap = TileMap(32)
        self.__background = Background(self.__screen.get_height())
        self.__game_interface = GameInterface(self)
        self.__game_interface.reset_timer()

        self.__tilemap.load("data/mapas/map1.json")
            
        for spawner in self.__tilemap.procurar_objeto([('Spawners', 0)]):

            print(spawner["pos"])
            if spawner['variant'] == 0:
                self.__player.pos = spawner['pos']


        try:
            self.__background = Background.load("data/backgrounds/default.json")
        except FileNotFoundError:
            pass
        
        

        self.__spawn_manager = SpawnManager(self.__tilemap, self.__player, self.__num_inimigos, game=self)
        self.__spawn_manager.spawn_todos_inimigos()
        self.__tocar_musica_aleatoria()

    def __player_morreu(self):
        tempo_jogo = None
        if self.__game_interface:
            tempo_atual = pygame.time.get_ticks()
            tempo_jogo = (tempo_atual - self.__game_interface._GameInterface__start_time) // 1000
        self.__remover_progresso()  # Remove o save ao dar game over, se for do mesmo jogador
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
        self.__remover_progresso()  # Remove o save ao vencer, se for do mesmo jogador
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
        self.__atualizar_Particulas(camera_movement)
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
        if self.__player.vida <= 0:
            self.__player_morreu()
        elif self.__spawn_manager and self.__spawn_manager.get_inimigos_vivos() == 0:
            self.__player_venceu()

    def __salvar_progresso(self):
        if not self.__player:
            return False
        # Salvar inimigos vivos (posição e estado)
        inimigos_vivos = []
        if self.__spawn_manager:
            for inimigo in self.__spawn_manager._SpawnManager__inimigos_ativos:
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
            "nome": self.__nome_jogador,
            "dificuldade": self.__dificuldade,
            "num_inimigos": self.__num_inimigos,
            "player": {
                "pos": list(self.__player.pos),
                "vida": self.__player.vida,
                "vidaMax": self.__player.vidaMax,
                "furia": self.__player.furia,
                "estado": self.__player.estado,
                "pulos_disponiveis": self.__player.pulos_disponiveis,
            },
            "tempo": self.__game_interface.get_tempo() if self.__game_interface else 0,
            "inimigos_vivos": self.__spawn_manager.get_inimigos_vivos() if self.__spawn_manager else 0,
            "inimigos_mortos": self.__spawn_manager.get_inimigos_mortos() if self.__spawn_manager else 0,
            "inimigos_totais": self.__spawn_manager.get_total_inimigos() if self.__spawn_manager else 0,
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
                if progresso.get("nome") == self.__nome_jogador:
                    os.remove(save_path)
            except Exception:
                pass

    def iniciar_jogo_carregado(self):
        progresso = self.__carregar_progresso()
        if not progresso:
            return
        self.__nome_jogador = progresso["nome"]
        self.__dificuldade = progresso["dificuldade"]
        self.__num_inimigos = progresso["num_inimigos"]
        self.__inicializar_componentes_jogo()
        # Restaurar player
        p = progresso["player"]
        self.__player.pos = p["pos"]
        self.__player.vida = p["vida"]
        self.__player.vidaMax = p["vidaMax"]
        self.__player.furia = p["furia"]
        self.__player.estado = p["estado"]
        self.__player.pulos_disponiveis = p["pulos_disponiveis"]
        # Restaurar tempo
        if self.__game_interface:
            self.__game_interface.set_tempo(progresso.get("tempo", 0))
        # Restaurar inimigos ativos
        if self.__spawn_manager:
            self.__spawn_manager._SpawnManager__inimigos_ativos.clear()
            for inimigo_data in progresso.get("inimigos_ativos", []):
                if inimigo_data['tipo'] == 'Slime':
                    from entidades.slime import Slime
                    inimigo = Slime(tuple(inimigo_data['pos']), (16, 16))
                    # Restaurar propriedades do slime
                    inimigo.vida = inimigo_data.get('vida', 1)
                    inimigo.estado = inimigo_data.get('estado', 'idle')
                    self.__spawn_manager._SpawnManager__inimigos_ativos.append(inimigo)
                elif inimigo_data['tipo'] == 'Esqueleto':
                    from entidades.esqueleto import Esqueleto
                    inimigo = Esqueleto(tuple(inimigo_data['pos']), (32, 32), game=self)
                    # Restaurar propriedades do esqueleto
                    inimigo.vida = inimigo_data.get('vida', 2)
                    inimigo.vida_maxima = inimigo_data.get('vida_maxima', 2)
                    inimigo.estado = inimigo_data.get('estado', 'inativo')
                    self.__spawn_manager._SpawnManager__inimigos_ativos.append(inimigo)
            self.__spawn_manager._SpawnManager__inimigos_mortos = progresso.get("inimigos_mortos", 0)
            self.__spawn_manager._SpawnManager__max_inimigos = len(progresso.get("inimigos_ativos", []))
            self.__spawn_manager._SpawnManager__inimigos_totais = progresso.get("inimigos_totais", self.__num_inimigos)
        self.__estado = "jogando"

    def mostrar_menu_pausa(self):
        largura, altura = self.__screen.get_size()
        fonte = pygame.font.SysFont("Arial", 32, bold=True)
        opcoes = ["Salvar", "Sair", "Voltar"]
        selecionado = 0
        rodando = True
        mensagem = ""
        tempo_pausado = 0
        if self.__game_interface:
            tempo_pausado = self.__game_interface.get_tempo()
        while rodando:
            self.__screen.fill((25, 25, 35))
            titulo = fonte.render("PAUSADO", True, (64, 224, 208))
            self.__screen.blit(titulo, (largura // 2 - titulo.get_width() // 2, 120))
            for i, texto in enumerate(opcoes):
                cor = (255, 99, 71) if i == selecionado else (240, 240, 240)
                botao = fonte.render(texto, True, cor)
                self.__screen.blit(botao, (largura // 2 - botao.get_width() // 2, 220 + i * 70))
            if mensagem:
                msg_surf = fonte.render(mensagem, True, (0,255,0))
                self.__screen.blit(msg_surf, (largura // 2 - msg_surf.get_width() // 2, 450))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
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
                            if self.__game_interface:
                                self.__game_interface.set_tempo(tempo_pausado)
                    elif event.key == pygame.K_ESCAPE:
                        rodando = False
                        mensagem = ""
                        if self.__game_interface:
                            self.__game_interface.set_tempo(tempo_pausado)
        return None

    def processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if self.__estado == "jogando" and event.key == pygame.K_ESCAPE:
                    acao = self.mostrar_menu_pausa()
                    if acao == "sair":
                        self.__estado = "menu"
                        self.__menu.voltar_menu_principal()
                else:
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
                elif key == pygame.K_p:
                    self.__toggle_pausar_musica()
                elif key == pygame.K_PLUS or key == pygame.K_KP_PLUS:
                    self.__ajustar_volume_musica(0.1)
                elif key == pygame.K_MINUS or key == pygame.K_KP_MINUS:
                    self.__ajustar_volume_musica(-0.1)
            else:
                if key == pygame.K_RIGHT:
                    self.__player.mover_direita(False)
                elif key == pygame.K_LEFT:
                    self.__player.mover_esquerda(False)

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