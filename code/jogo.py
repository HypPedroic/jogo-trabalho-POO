# Importanto as bibliotecas necessárias
import pygame
import sys
import os

# Importando as classes necessárias
from entidades.jogador import Jogador
from entidades.inimigo_terrestre import InimigoTerrestre
from entidades.projetil import Projetil
from tilemap.tile_map import TileMap
from background.background import Background
from ui.menu import Menu
from ui.hud import HUD
from nivel.nivel import Nivel

# Importando as funções necessárias
from utils.utils import load_image, load_images

# Classe do jogo
class Jogo:

    # Inicializando o jogo
    def __init__(self):
        pygame.init()
        # Aumentando o tamanho da tela para uma resolução mais moderna
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Jump & Dash")
        # Mantendo a mesma proporção para o display de renderização
        self.display = pygame.Surface((512, 384))
        self.clock = pygame.time.Clock()
        self.running = True
        self.estado = 'menu'  # 'menu', 'jogando', 'game_over'
        
        self.movimento = [False, False]
        self.atacando = False
        
        # Carregando as imagens
        self.carregar_assets()

        # Inicializando componentes
        self.tilemap = TileMap(self, 32)
        self.camera = [0, 0]
        self.background = Background(self)
        self.menu = Menu(self)
        self.hud = HUD(self)
        
        # Listas de entidades
        self.inimigos = []
        self.projeteis = []
        
        # Inicializa o jogador (será criado quando o jogo começar)
        self.player = None
        
        # Inicializa o nível (será criado quando o jogo começar)
        self.nivel = None
        
        # Adiciona as camadas de fundo
        self.inicializar_background()
    
    def carregar_assets(self):
        """Carrega todos os assets do jogo"""
        self.assets = {
            # Tiles
            'grass': load_images('tiles/grama'),
            
            # Jogador
            'player': {
                'parado': [load_image('player/player.png')],  # Temporário, deve ser substituído por animações
                'correndo': [load_image('player/player.png')],  # Temporário
                'pulando': [load_image('player/player.png')],  # Temporário
                'caindo': [load_image('player/player.png')]   # Temporário
            },
            
            # Inimigos
            'inimigo_terrestre': {
                'parado': [pygame.image.load('data/images/enemy/inimigo-parado.gif').convert_alpha()],
                'correndo': [pygame.image.load('data/images/enemy/inimigo-correndo.gif').convert_alpha()],
                'atacando': [pygame.image.load('data/images/enemy/inimigo-atacando.gif').convert_alpha()]
            },
            'inimigo_suicida': {
                'parado': [pygame.image.load('data/images/enemy/inimigo-parado.gif').convert_alpha()],
                'correndo': [pygame.image.load('data/images/enemy/inimigo-correndo.gif').convert_alpha()],
                'explodindo': [pygame.image.load('data/images/enemy/inimigo-morendo.gif').convert_alpha()]
            },
            
            # Projéteis
            'projetil_jogador': [load_image('player/player.png')],  # Temporário
            'projetil_inimigo': [load_image('player/player.png')],  # Temporário
            
            # Background
            'background': load_image('background/Background.png')
        }
    
    def inicializar_background(self):
        """Inicializa as camadas de fundo"""
        self.background.add_layer('background/Layers/1.png', 0.1)
        self.background.add_layer('background/Layers/2.png', 0.3)
        self.background.add_layer('background/Layers/3.png', 0.5)
        self.background.add_layer('background/Layers/4.png', 0.7)
        self.background.add_layer('background/Layers/5.png', 0.9)
    
    def iniciar_jogo(self):
        """Inicia um novo jogo"""
        # Muda o estado para 'jogando'
        self.estado = 'jogando'
        
        # Cria o jogador
        self.player = Jogador(self, (50, 300))
        
        # Cria o nível
        self.nivel = Nivel(self)
        
        # Limpa as listas de entidades
        self.inimigos = []
        self.projeteis = []
        
        # Reseta a câmera
        self.camera = [0, 0]
    
    def game_over(self):
        """Finaliza o jogo atual e mostra a tela de game over"""
        # Adiciona a pontuação ao ranking
        self.menu.adicionar_pontuacao(self.player.distancia_percorrida * 0.1)  # Converte para metros
        
        # Muda o estado para 'game_over'
        self.estado = 'game_over'
        self.menu.estado = 'game_over'
        self.menu.opcao_selecionada = 0
    
    def processar_eventos(self):
        """Processa os eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.estado == 'menu' or self.estado == 'game_over':
                # Passa os eventos para o menu
                self.menu.processar_eventos([event])
            
            elif self.estado == 'jogando':
                # Processa os eventos do jogo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.movimento[0] = True
                    elif event.key == pygame.K_LEFT:
                        self.movimento[1] = True
                    if event.key == pygame.K_UP:
                        # Pulo normal se estiver no chão
                        if self.player._pode_pular:
                            self.player.pular()
                        # Pulo duplo se estiver no ar e tiver pulo duplo disponível
                        elif self.player.pulo_duplo_disponivel:
                            self.player.pular()
                    if event.key == pygame.K_SPACE:
                        self.atacando = True
                        self.player.atacar()
                    if event.key == pygame.K_ESCAPE:
                        # Pausa o jogo e volta para o menu
                        self.estado = 'menu'
                        self.menu.estado = 'menu_principal'
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movimento[0] = False
                    elif event.key == pygame.K_LEFT:
                        self.movimento[1] = False
                    if event.key == pygame.K_SPACE:
                        self.atacando = False
    
    def atualizar(self):
        """Atualiza o estado do jogo"""
        if self.estado == 'jogando':
            # Atualiza o nível
            self.nivel.update()
            
            # Atualiza o jogador
            self.player.update((self.movimento[0] - self.movimento[1], 0))
            
            # Verifica se o jogador morreu
            if not self.player.vivo:
                self.game_over()
                return
            
            # Atualiza os inimigos
            for inimigo in self.inimigos.copy():
                inimigo.update()
                if not inimigo.ativo:
                    self.inimigos.remove(inimigo)
            
            # Atualiza os projéteis
            for projetil in self.projeteis.copy():
                projetil.update()
                if not projetil.ativo:
                    self.projeteis.remove(projetil)
            
            # Atualiza a câmera para seguir o jogador
            self.camera[0] += (self.player.retangulo().centerx - self.display.get_width() / 2 - self.camera[0]) / 16
            self.camera[1] += (self.player.retangulo().centery - self.display.get_height() / 2 - self.camera[1]) / 16
            
            # Atualiza o background
            self.background.update(self.camera)
    
    def renderizar(self):
        """Renderiza o jogo na tela"""
        # Limpa a tela
        self.display.fill((0, 0, 0))
        
        if self.estado == 'menu' or self.estado == 'game_over':
            # Renderiza o menu
            self.menu.renderizar(self.screen)
        
        elif self.estado == 'jogando':
            # Renderiza o background
            self.background.render(self.display)
            
            # Calcula o offset da câmera
            camera_offset = (int(self.camera[0]), int(self.camera[1]))
            
            # Renderiza o tilemap
            self.tilemap.renderizar(self.display, offset=camera_offset)
            
            # Renderiza os projéteis
            for projetil in self.projeteis:
                projetil.renderizar(self.display, offset=camera_offset)
            
            # Renderiza os inimigos
            for inimigo in self.inimigos:
                inimigo.renderizar(self.display, offset=camera_offset)
            
            # Renderiza o jogador
            self.player.renderizar(self.display, offset=camera_offset)
            
            # Renderiza o HUD
            self.hud.renderizar(self.display)
            
            # Escala a superfície de exibição para a tela
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            # Processa os eventos
            self.processar_eventos()
            
            # Atualiza o estado do jogo
            self.atualizar()
            
            # Renderiza o jogo
            self.renderizar()
            
            # Atualiza a tela
            pygame.display.flip()
            
            # Controla o FPS
            self.clock.tick(60)
        
        # Finaliza o pygame
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()
