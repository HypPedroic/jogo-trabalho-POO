# Importanto as bibliotecas necessárias
import pygame
import sys
import random
import os


# Importando as classes necessárias
from entidades.player import Player
from entidades.spawn_manager import SpawnManager
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
        self.__screen = pygame.display.set_mode((832, 640))
        self.__display = pygame.Surface((624, 480))
        pygame.display.set_caption("ReaperQuest 💀")
        self.__clock = pygame.time.Clock()
        self.__running = True
        self.__camera = [0, 0]

        # Estados do jogo
        self.__estado = "menu"  # menu, jogando, game_over
        self.__nome_jogador = ""

        # Menu moderno
        self.__menu = MenuModerno(self.__screen)
        self.__menu.callback_iniciar_jogo = self.iniciar_jogo

        # Componentes do jogo (inicializados quando necessário)
        self.__player = None
        self.__tilemap = None
        self.__background = None
        self.__game_interface = None
        self.__spawn_manager = None

        # Sistema de limbo
        self.__limite_mapa_y = 1000  # Distância abaixo do mapa onde o player morre
        self.__mapa_min_y = 0  # Será calculado baseado no tilemap
        
        self.projeteis = []  # Lista de projéteis no jogo
        self.inimigos = [] # Lista de inimigos no jogo
        
        # Sistema de áudio
        self.__musicas = [
            "01 Blossom Tree.wav",
            "03 Himawari No Sato.wav", 
            "04 Whispering Stars.wav",
            "06 Tengu.wav",
            "07 Gion District.wav",
            "08 Higanbana Field.wav"
        ]
        self.__sons = {}
        self.__carregar_sons()
        


    # Properties para atributos que precisam ser acessados externamente
    @property
    def screen(self):
        return self.__screen

    @property
    def display(self):
        return self.__display

    @property
    def clock(self):
        return self.__clock

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, value):
        self.__running = value

    @property
    def camera(self):
        return self.__camera

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
    def menu(self):
        return self.__menu

    @property
    def player(self):
        return self.__player

    @property
    def tilemap(self):
        return self.__tilemap

    @property
    def background(self):
        return self.__background

    @property
    def game_interface(self):
        return self.__game_interface

    def iniciar_jogo(self, dados_jogo):
        """Inicia um novo jogo com o nome do jogador e configurações de dificuldade"""
        self.nome_jogador = dados_jogo['nome']
        self.__dificuldade = dados_jogo['dificuldade']
        self.__num_inimigos = dados_jogo['num_inimigos']
        # Reset da flag para evitar duplicação no ranking
        if hasattr(self, '__ranking_adicionado'):
            delattr(self, '__ranking_adicionado')
        self.__inicializar_componentes_jogo()
        self.estado = "jogando"

    def __carregar_sons(self):
        """Carrega todos os efeitos sonoros"""
        try:
            self.__sons['tiro'] = pygame.mixer.Sound("data/sounds/sound-tiro.wav")
            self.__sons['ataque'] = pygame.mixer.Sound("data/sounds/sound-ataque.wav")
            self.__sons['dano'] = pygame.mixer.Sound("data/sounds/sound-tomando-dano.wav")
            self.__sons['matando_inimigo'] = pygame.mixer.Sound("data/sounds/sound-matando-inimigo.wav")
            self.__sons['furia'] = pygame.mixer.Sound("data/sounds/sound-puxando-foice-furia.wav")
        except pygame.error as e:
            print(f"Erro ao carregar sons: {e}")
    
    def __tocar_musica_aleatoria(self):
        """Toca uma música de fundo aleatória"""
        try:
            musica_escolhida = random.choice(self.__musicas)
            caminho_musica = f"data/music/{musica_escolhida}"
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.set_volume(0.3)  # Volume baixo para não atrapalhar
            pygame.mixer.music.play(-1)  # Loop infinito
            print(f"Tocando música: {musica_escolhida}")
        except pygame.error as e:
            print(f"Erro ao carregar música: {e}")
    
    def tocar_som(self, nome_som):
        """Toca um efeito sonoro específico"""
        if nome_som in self.__sons:
            try:
                self.__sons[nome_som].play()
            except pygame.error as e:
                print(f"Erro ao tocar som {nome_som}: {e}")

    def __inicializar_componentes_jogo(self):
        """Inicializa todos os componentes necessários para o jogo"""
        # Inicializa o player
        self.__player = Player((0, 0), (20, 32))

        # Inicializa o tilemap
        self.__tilemap = TileMap(32)
        try:
            self.__tilemap.load("data/mapas/map.json")
            # Calcula o limite inferior do mapa
            self.__calcular_limite_mapa()
        except FileNotFoundError:
            print("Mapa não encontrado, usando configuração padrão")
            self.__mapa_min_y = 0
            

        # Inicializa o background
        self.__background = Background(self.__screen.get_height())
        try:
            self.__background = Background.load("data/backgrounds/default.json")
        except FileNotFoundError:
            pass

        # Inicializa a interface do jogo
        self.__game_interface = GameInterface(self)
        self.__game_interface.reset_timer()
        
        # Inicializa o spawn manager com a quantidade de inimigos baseada na dificuldade
        self.__spawn_manager = SpawnManager(self.__tilemap, self.__player, self.__num_inimigos)
        self.__spawn_manager.game = self  # Passa referência do game
        self.__spawn_manager.spawn_todos_inimigos()  # Spawna todos os inimigos de uma vez
        
        # Inicia música de fundo aleatória
        self.__tocar_musica_aleatoria()

    def __calcular_limite_mapa(self):
        """Calcula o limite inferior do mapa baseado nos tiles"""
        if self.__tilemap and hasattr(self.__tilemap, "tilemap"):
            max_y = 0
            for pos_str in self.__tilemap.tilemap:
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
            self.__mapa_min_y = (max_y + 1) * self.__tilemap.tile_size
            self.__limite_mapa_y = self.__mapa_min_y + 500
        else:
            # Valor padrão se não houver tilemap
            self.__limite_mapa_y = 1000

    def __verificar_limbo(self):
        """Verifica se o player caiu no limbo"""
        if self.__player and self.__player.retangulo().y > self.__limite_mapa_y:
            self.__player_morreu()

    def __player_morreu(self):
        """Chamado quando o player morre"""
        tempo_jogo = None
        if self.__game_interface:
            tempo_atual = pygame.time.get_ticks()
            tempo_jogo = (tempo_atual - self.__game_interface._GameInterface__start_time) // 1000

        self.__estado = "game_over"
        self.__menu.mostrar_game_over(tempo_jogo)
        
    def __player_venceu(self):
        """Chamado quando o player vence (derrota todos os inimigos)"""
        tempo_jogo = None
        if self.__game_interface:
            tempo_atual = pygame.time.get_ticks()
            tempo_jogo = (tempo_atual - self.__game_interface._GameInterface__start_time) // 1000
            
        # Para a música
        pygame.mixer.music.stop()
        
        # Estatísticas do jogo
        estatisticas = {
            'tempo': tempo_jogo,
            'inimigos_mortos': self.__spawn_manager.get_inimigos_mortos() if self.__spawn_manager else 0,
            'total_inimigos': self.__spawn_manager.get_total_inimigos() if self.__spawn_manager else 0,
            'vida_restante': self.__player.vida if self.__player else 0,
            'vida_maxima': self.__player.vidaMax if self.__player else 0
        }
        
        # O tempo será adicionado ao ranking na tela de vitória
            
        self.__estado = "vitoria"
        if hasattr(self.__menu, 'mostrar_vitoria'):
            self.__menu.mostrar_vitoria(tempo_jogo, estatisticas)
        else:
            # Fallback - mostra tela simples de vitória
             self.__mostrar_tela_vitoria_simples(estatisticas)
    
    def __mostrar_tela_vitoria_simples(self, estatisticas):
        """Mostra uma tela moderna de vitória com estatísticas"""
        # Cores modernas (mesmo esquema do menu)
        cor_primaria = (64, 224, 208)  # Turquesa
        cor_acento = (255, 99, 71)  # Coral
        cor_base = (25, 25, 35)  # Azul escuro
        cor_botao = (45, 45, 60)
        cor_botao_hover = (65, 65, 85)
        cor_texto = (240, 240, 240)
        cor_texto_secundario = (180, 180, 180)
        
        # Fontes modernas
        try:
            fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)
            fonte_subtitulo = pygame.font.SysFont("Arial", 24)
            fonte_botao = pygame.font.SysFont("Arial", 20, bold=True)
            fonte_texto = pygame.font.SysFont("Arial", 18)
        except:
            fonte_titulo = pygame.font.Font(None, 48)
            fonte_subtitulo = pygame.font.Font(None, 24)
            fonte_botao = pygame.font.Font(None, 20)
            fonte_texto = pygame.font.Font(None, 18)
        
        # Botão para voltar ao menu
        largura_tela = self.__screen.get_width()
        altura_tela = self.__screen.get_height()
        botao_rect = pygame.Rect(largura_tela // 2 - 120, altura_tela - 100, 240, 50)
        
        # Animação simples
        tempo_animacao = pygame.time.get_ticks() // 10
        
        # Loop principal da tela de vitória
        aguardando = True
        botao_selecionado = False
        
        while aguardando:
            mouse_pos = pygame.mouse.get_pos()
            botao_hover = botao_rect.collidepoint(mouse_pos)
            
            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_RETURN:
                        aguardando = False
                        self.__estado = "menu"
                        self.__menu.estado = "menu_principal"
                        self.__menu.voltar_menu_principal()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_hover:
                        aguardando = False
                        self.__estado = "menu"
                        self.__menu.estado = "menu_principal"
                        self.__menu.voltar_menu_principal()
            
            # Desenha fundo gradiente
            for y in range(altura_tela):
                cor_r = int(15 + (y / altura_tela) * 10)
                cor_g = int(15 + (y / altura_tela) * 10)
                cor_b = int(25 + (y / altura_tela) * 15)
                pygame.draw.line(self.__screen, (cor_r, cor_g, cor_b), (0, y), (largura_tela, y))
            
            # Desenha partículas animadas
            for i in range(20):
                x = (i * 137 + tempo_animacao) % largura_tela
                y = (i * 73 + tempo_animacao // 2) % altura_tela
                alpha = 50 + 30 * (i % 3)
                if alpha > 255:
                    alpha = 255
                pygame.draw.circle(self.__screen, (255, 255, 255), (int(x), int(y)), 1)
            
            # Título principal com efeito de brilho
            titulo = fonte_titulo.render("PARABENS!", True, cor_primaria)
            titulo_rect = titulo.get_rect(center=(largura_tela // 2, 80))
            # Sombra do título
            titulo_sombra = fonte_titulo.render("PARABENS!", True, (0, 0, 0))
            sombra_rect = titulo_sombra.get_rect(center=(largura_tela // 2 + 3, 83))
            self.__screen.blit(titulo_sombra, sombra_rect)
            self.__screen.blit(titulo, titulo_rect)
            
            # Subtítulo
            subtitulo = fonte_subtitulo.render("Missão Concluída com Sucesso!", True, cor_texto)
            subtitulo_rect = subtitulo.get_rect(center=(largura_tela // 2, 130))
            self.__screen.blit(subtitulo, subtitulo_rect)
            
            # Painel de estatísticas com fundo
            painel_rect = pygame.Rect(largura_tela // 2 - 200, 180, 400, 220)
            pygame.draw.rect(self.__screen, (35, 35, 50), painel_rect, border_radius=15)
            pygame.draw.rect(self.__screen, cor_primaria, painel_rect, 3, border_radius=15)
            
            # Título do painel
            titulo_stats = fonte_subtitulo.render("ESTATÍSTICAS DA MISSÃO", True, cor_primaria)
            titulo_stats_rect = titulo_stats.get_rect(center=(largura_tela // 2, 200))
            self.__screen.blit(titulo_stats, titulo_stats_rect)
            
            # Estatísticas
            y_pos = 240
            estatisticas_texto = [
                ("Tempo:", f"{estatisticas['tempo']}s" if estatisticas['tempo'] else "--"),
                ("Inimigos:", f"{estatisticas['inimigos_mortos']}/{estatisticas['total_inimigos']}"),
                ("Vida:", f"{estatisticas['vida_restante']}/{estatisticas['vida_maxima']}")
            ]
            
            for label, valor in estatisticas_texto:
                # Label
                label_surface = fonte_texto.render(label, True, cor_texto_secundario)
                self.__screen.blit(label_surface, (largura_tela // 2 - 150, y_pos))
                
                # Valor
                valor_surface = fonte_texto.render(valor, True, cor_texto)
                valor_rect = valor_surface.get_rect(right=largura_tela // 2 + 150)
                valor_rect.y = y_pos
                self.__screen.blit(valor_surface, valor_rect)
                
                y_pos += 35
            
            # Mensagem de ranking
            if estatisticas['tempo'] and hasattr(self.__menu, 'adicionar_ao_ranking'):
                # Adiciona ao ranking apenas uma vez
                if not hasattr(self, '__ranking_adicionado'):
                    self.__menu.adicionar_ao_ranking(self.__nome_jogador, estatisticas['tempo'])
                    self.__ranking_adicionado = True
                ranking_texto = fonte_texto.render("Tempo adicionado ao ranking!", True, cor_acento)
                ranking_rect = ranking_texto.get_rect(center=(largura_tela // 2, y_pos + 20))
                self.__screen.blit(ranking_texto, ranking_rect)
            
            # Botão moderno para voltar ao menu
            cor_botao_atual = cor_botao_hover if botao_hover else cor_botao
            
            # Sombra do botão
            sombra_botao = botao_rect.copy()
            sombra_botao.x += 3
            sombra_botao.y += 3
            pygame.draw.rect(self.__screen, (0, 0, 0), sombra_botao, border_radius=10)
            
            # Botão principal
            pygame.draw.rect(self.__screen, cor_botao_atual, botao_rect, border_radius=10)
            
            # Borda se hover
            if botao_hover:
                pygame.draw.rect(self.__screen, cor_primaria, botao_rect, 2, border_radius=10)
            
            # Texto do botão
            texto_botao = fonte_botao.render("VOLTAR AO MENU", True, cor_texto)
            texto_botao_rect = texto_botao.get_rect(center=botao_rect.center)
            self.__screen.blit(texto_botao, texto_botao_rect)
            
            # Instrução adicional
            instrucao = fonte_texto.render("Pressione ESC ou ENTER para continuar", True, cor_texto_secundario)
            instrucao_rect = instrucao.get_rect(center=(largura_tela // 2, altura_tela - 30))
            self.__screen.blit(instrucao, instrucao_rect)
            
            pygame.display.flip()
            tempo_animacao += 1

    def inicializar_jogo(self):
        """Método mantido para compatibilidade"""
        self.__estado = "jogando"

    def __rodar_jogo(self):
        # Verifica se os componentes estão inicializados
        if (
            not self.__player
            or not self.__tilemap
            or not self.__background
            or not self.__game_interface
        ):
            return

        self.__display.fill((52, 222, 235))

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
        camera_movement = (int(self.__camera[0]), int(self.__camera[1]))

        # Atualiza e renderiza o background
        self.__background.update(self.__camera)
        self.__background.render(self.__display)

        self.__tilemap.renderizar(self.__display, offset=camera_movement)

        self.__player.update(self.__tilemap, self)
        self.__player.renderizar(self.__display, offset=camera_movement)
        
        # Atualiza e renderiza inimigos
        if self.__spawn_manager:
            self.__spawn_manager.update()
            self.__spawn_manager.render(self.__display, camera_movement)
            
            # Verifica colisões entre projéteis e inimigos
            self.__spawn_manager.verificar_colisoes_projeteis(self.projeteis)
        
        for projetil in self.projeteis:
            projetil.update(self, self.__tilemap)
            projetil.renderizar(self.__display, offset=camera_movement)
            if projetil.vida <= 0:
                self.projeteis.remove(projetil)

        # Verifica se o player caiu no limbo
        self.__verificar_limbo()

        # Verifica se o player morreu (vida zero)
        if self.__player.vida <= 0:
            self.__player_morreu()
            return
            
        # Verifica se todos os inimigos foram derrotados
        if self.__spawn_manager and self.__spawn_manager.get_inimigos_vivos() == 0:
            self.__player_venceu()
            return

        # Renderiza a interface do jogo
        self.__game_interface.render(self.__display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.constants.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.__player.mover_direita(True)
                elif event.key == pygame.K_LEFT:
                    self.__player.mover_esquerda(True)
                if event.key == pygame.K_UP:
                    self.__player.pular()
                if event.key == pygame.K_q:
                    self.__player.ativar_furia(self)
                if event.key == pygame.K_SPACE:
                    self.__player.atacar()
                # Tecla ESC para voltar ao menu
                if event.key == pygame.K_ESCAPE:
                    self.__estado = "menu"
                    self.__menu.voltar_menu_principal()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.__player.mover_direita(False)
                elif event.key == pygame.K_LEFT:
                    self.__player.mover_esquerda(False)

        self.__screen.blit(
            pygame.transform.scale(self.__display, self.__screen.get_size()), (0, 0)
        )
        pygame.display.flip()
        self.__clock.tick(60)

    def run(self):
        try:
            while self.__running:
                if self.__estado == "menu":
                    print("Executando menu...")
                    # Executa o menu e verifica se deve continuar
                    self.__menu.running = True
                    nome = self.__menu.run()
                    print(f"Menu retornou: {nome}")
                    if nome:  # Se retornou um nome, inicia o jogo
                        print(f"Iniciando jogo com jogador: {nome}")
                        self.iniciar_jogo(nome)
                    elif not self.__menu.running:  # Se o menu foi fechado
                        print("Menu foi fechado, encerrando jogo")
                        self.__running = False
                    else:
                        print("Menu continua rodando...")
                elif self.__estado == "jogando":
                    self.__rodar_jogo()
                elif self.__estado == "game_over":
                    print("Executando menu de game over...")
                    # Executa o menu de game over
                    self.__menu.running = True
                    self.__menu.run()
                    if not self.__menu.running:  # Se o menu foi fechado
                        print("Menu de game over foi fechado")
                        # Verifica se deve voltar ao menu principal ou sair
                        if self.__menu.estado == "menu_principal":
                            self.__estado = "menu"
                            print("Voltando ao menu principal")
                        else:
                            self.__running = False
                elif self.__estado == "vitoria":
                    print("Executando tela de vitória...")
                    # Executa a tela de vitória
                    self.__menu.running = True
                    self.__menu.run()
                    if not self.__menu.running:  # Se o menu foi fechado
                        print("Tela de vitória foi fechada")
                        # Verifica se deve voltar ao menu principal ou sair
                        if self.__menu.estado == "menu_principal":
                            self.__estado = "menu"
                            print("Voltando ao menu principal")
                        else:
                            self.__running = False
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
