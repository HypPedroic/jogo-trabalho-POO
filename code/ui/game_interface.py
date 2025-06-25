import pygame
import os


class GameInterface:
    """Classe responsável pela interface visual do jogo (corações, pulo, fúria)"""

    def __init__(self, game):
        self.__game = game
        self.__images = {}
        self.__load_images()

        # Posições dos elementos na tela
        self.__hearts_start_x = 20
        self.__hearts_y = 20
        self.__heart_spacing = 40

        self.__jump_orb_x = 160
        self.__jump_orb_y = 20

        self.__fury_bar_x = 220
        self.__fury_bar_y = 20
        self.__fury_bar_width = 200
        self.__fury_bar_height = 20

        # Timer do jogo
        self.__start_time = pygame.time.get_ticks()
        self.__font = pygame.font.Font(None, 36)
        self.__timer_color = (255, 255, 255)
    
    @property
    def game(self):
        return self.__game

    def __load_images(self):
        """Carrega as imagens da interface"""
        base_path = "data/images/interface/"

        try:
            # Verifica se pygame está inicializado
            if not pygame.get_init():
                pygame.init()

            # Carrega a imagem do coração
            self.__images["heart"] = pygame.image.load(
                base_path + "coracao.png"
            ).convert_alpha()

            # Carrega as imagens do pulo (disponível e indisponível)
            self.__images["jump_available"] = pygame.image.load(
                base_path + "puloV.png"
            ).convert_alpha()
            self.__images["jump_unavailable"] = pygame.image.load(
                base_path + "puloF.png"
            ).convert_alpha()

            # Redimensiona as imagens se necessário
            self.__images["heart"] = pygame.transform.scale(
                self.__images["heart"], (32, 32)
            )
            self.__images["jump_available"] = pygame.transform.scale(
                self.__images["jump_available"], (32, 32)
            )
            self.__images["jump_unavailable"] = pygame.transform.scale(
                self.__images["jump_unavailable"], (32, 32)
            )

        except (pygame.error, FileNotFoundError) as e:
            print(f"Erro ao carregar imagens da interface: {e}")
            print("Usando imagens de fallback...")
            # Cria imagens de fallback se não conseguir carregar
            self.__create_fallback_images()

    def __create_fallback_images(self):
        """Cria imagens de fallback caso não consiga carregar as originais"""
        # Coração vermelho
        heart_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(heart_surf, (255, 0, 0), (16, 16), 15)
        self.__images["heart"] = heart_surf

        # Pulo disponível (azul)
        jump_available_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(jump_available_surf, (0, 150, 255), (16, 16), 15)
        self.__images["jump_available"] = jump_available_surf

        # Pulo indisponível (cinza)
        jump_unavailable_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(jump_unavailable_surf, (100, 100, 100), (16, 16), 15)
        self.__images["jump_unavailable"] = jump_unavailable_surf

        # Não precisamos mais da imagem de fúria

    def __render_hearts(self, surface):
        """Renderiza os corações de vida"""
        player_life = self.__game.player.vida
        max_life = self.__game.player.vidaMax

        for i in range(max_life):
            x = self.__hearts_start_x + (i * self.__heart_spacing)
            y = self.__hearts_y

            if i < player_life:
                # Coração cheio
                surface.blit(self.__images["heart"], (x, y))
            else:
                # Coração vazio (mais transparente)
                heart_copy = self.__images["heart"].copy()
                heart_copy.set_alpha(80)
                surface.blit(heart_copy, (x, y))

    def __render_jump_orb(self, surface):
        """Renderiza a bolinha do pulo"""
        # Verifica se o pulo duplo está disponível
        if (
            hasattr(self.__game.player, "pulos_disponiveis")
            and self.__game.player.pulos_disponiveis > 0
        ):
            surface.blit(
                self.__images["jump_available"], (self.__jump_orb_x, self.__jump_orb_y)
            )
        else:
            surface.blit(
                self.__images["jump_unavailable"], (self.__jump_orb_x, self.__jump_orb_y)
            )

    def __render_fury_bar(self, surface):
        """Renderiza a barra de fúria"""
        # Desenha o fundo da barra
        background_rect = pygame.Rect(
            self.__fury_bar_x,
            self.__fury_bar_y,
            self.__fury_bar_width,
            self.__fury_bar_height,
        )
        pygame.draw.rect(surface, (50, 50, 50), background_rect)
        pygame.draw.rect(surface, (255, 255, 255), background_rect, 2)

        # Calcula o nível de fúria baseado no estado do player
        fury_level = self.game.player.furia/100
            

        # Desenha a barra de fúria - sempre vermelha quando ativa
        if fury_level > 0:
            fury_width = int(self.__fury_bar_width * fury_level)
            fury_rect = pygame.Rect(
                self.__fury_bar_x, self.__fury_bar_y, fury_width, self.__fury_bar_height
            )
            # Sempre vermelha quando usando a foice (Q)
            pygame.draw.rect(surface, (255, 0, 0), fury_rect)

        # Adiciona texto "FÚRIA" ao lado da barra
        fury_text = pygame.font.Font(None, 24).render("", True, (255, 255, 255))
        surface.blit(fury_text, (self.__fury_bar_x - 60, self.__fury_bar_y - 2))

    def __render_timer(self, surface):
        """Renderiza o contador de tempo"""
        current_time = pygame.time.get_ticks()
        elapsed_time = (
            current_time - self.__start_time
        ) // 1000  # Converte para segundos

        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        time_text = f"{minutes:02d}:{seconds:02d}"
        text_surface = self.__font.render(time_text, True, self.__timer_color)

        # Posiciona o timer no canto superior direito
        timer_x = surface.get_width() - text_surface.get_width() - 20
        timer_y = 20

        surface.blit(text_surface, (timer_x, timer_y))
    
    def __render_enemy_counter(self, surface):
        """Renderiza o contador de inimigos vivos"""
        if hasattr(self.__game, '_GameManager__spawn_manager') and self.__game._GameManager__spawn_manager:
            inimigos_vivos = self.__game._GameManager__spawn_manager.get_inimigos_vivos()
            enemy_text = f"Inimigos: {inimigos_vivos}"
            text_surface = pygame.font.Font(None, 28).render(enemy_text, True, (255, 255, 255))
            
            # Posiciona abaixo do timer
            timer_x = surface.get_width() - text_surface.get_width() - 20
            timer_y = 50
            
            surface.blit(text_surface, (timer_x, timer_y))

    def render(self, surface):
        """Renderiza todos os elementos da interface"""
        self.__render_hearts(surface)
        self.__render_jump_orb(surface)
        self.__render_fury_bar(surface)
        self.__render_timer(surface)
        self.__render_enemy_counter(surface)

    def reset_timer(self):
        """Reseta o timer do jogo"""
        self.__start_time = pygame.time.get_ticks()
