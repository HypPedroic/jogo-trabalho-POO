import pygame
import os


class GameInterface:
    """Classe responsável pela interface visual do jogo (corações, pulo, fúria)"""

    def __init__(self, game):
        self.game = game
        self.images = {}
        self.load_images()

        # Posições dos elementos na tela
        self.hearts_start_x = 20
        self.hearts_y = 20
        self.heart_spacing = 40

        self.jump_orb_x = 160
        self.jump_orb_y = 20

        self.fury_bar_x = 220
        self.fury_bar_y = 20
        self.fury_bar_width = 200
        self.fury_bar_height = 20

        # Timer do jogo
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)
        self.timer_color = (255, 255, 255)

    def load_images(self):
        """Carrega as imagens da interface"""
        base_path = "data/images/interface/"

        try:
            # Verifica se pygame está inicializado
            if not pygame.get_init():
                pygame.init()

            # Carrega a imagem do coração
            self.images["heart"] = pygame.image.load(
                base_path + "coracao.png"
            ).convert_alpha()

            # Carrega as imagens do pulo (disponível e indisponível)
            self.images["jump_available"] = pygame.image.load(
                base_path + "puloV.png"
            ).convert_alpha()
            self.images["jump_unavailable"] = pygame.image.load(
                base_path + "puloF.png"
            ).convert_alpha()

            # Carrega a imagem da fúria
            self.images["fury"] = pygame.image.load(
                base_path + "furia.png"
            ).convert_alpha()

            # Redimensiona as imagens se necessário
            self.images["heart"] = pygame.transform.scale(
                self.images["heart"], (32, 32)
            )
            self.images["jump_available"] = pygame.transform.scale(
                self.images["jump_available"], (32, 32)
            )
            self.images["jump_unavailable"] = pygame.transform.scale(
                self.images["jump_unavailable"], (32, 32)
            )
            self.images["fury"] = pygame.transform.scale(self.images["fury"], (32, 32))

        except (pygame.error, FileNotFoundError) as e:
            print(f"Erro ao carregar imagens da interface: {e}")
            print("Usando imagens de fallback...")
            # Cria imagens de fallback se não conseguir carregar
            self.create_fallback_images()

    def create_fallback_images(self):
        """Cria imagens de fallback caso não consiga carregar as originais"""
        # Coração vermelho
        heart_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(heart_surf, (255, 0, 0), (16, 16), 15)
        self.images["heart"] = heart_surf

        # Pulo disponível (azul)
        jump_available_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(jump_available_surf, (0, 150, 255), (16, 16), 15)
        self.images["jump_available"] = jump_available_surf

        # Pulo indisponível (cinza)
        jump_unavailable_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(jump_unavailable_surf, (100, 100, 100), (16, 16), 15)
        self.images["jump_unavailable"] = jump_unavailable_surf

        # Fúria (laranja)
        fury_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(fury_surf, (255, 165, 0), (0, 0, 32, 32))
        self.images["fury"] = fury_surf

    def render_hearts(self, surface):
        """Renderiza os corações de vida"""
        player_life = self.game.player.vida
        max_life = self.game.player.vidaMax

        for i in range(max_life):
            x = self.hearts_start_x + (i * self.heart_spacing)
            y = self.hearts_y

            if i < player_life:
                # Coração cheio
                surface.blit(self.images["heart"], (x, y))
            else:
                # Coração vazio (mais transparente)
                heart_copy = self.images["heart"].copy()
                heart_copy.set_alpha(80)
                surface.blit(heart_copy, (x, y))

    def render_jump_orb(self, surface):
        """Renderiza a bolinha do pulo"""
        # Verifica se o pulo duplo está disponível
        # Como não vejo essa propriedade no player, vou usar uma lógica baseada no air_time
        if (
            hasattr(self.game.player, "_pulos_disponiveis")
            and self.game.player._pulos_disponiveis > 0
        ):
            surface.blit(
                self.images["jump_available"], (self.jump_orb_x, self.jump_orb_y)
            )
        else:
            surface.blit(
                self.images["jump_unavailable"], (self.jump_orb_x, self.jump_orb_y)
            )

    def render_fury_bar(self, surface):
        """Renderiza a barra de fúria"""
        # Desenha o ícone da fúria
        surface.blit(self.images["fury"], (self.fury_bar_x - 40, self.fury_bar_y))

        # Desenha o fundo da barra
        background_rect = pygame.Rect(
            self.fury_bar_x,
            self.fury_bar_y + 6,
            self.fury_bar_width,
            self.fury_bar_height,
        )
        pygame.draw.rect(surface, (50, 50, 50), background_rect)
        pygame.draw.rect(surface, (255, 255, 255), background_rect, 2)

        # Calcula o nível de fúria baseado no estado do player
        fury_level = 0.0
        if hasattr(self.game.player, "_estado"):
            if self.game.player._estado == "foice":
                fury_level = 1.0  # Fúria máxima quando em estado foice
            else:
                # Pode implementar uma lógica de acúmulo de fúria aqui
                fury_level = 0.3  # Exemplo: 30% de fúria

        # Desenha a barra de fúria
        if fury_level > 0:
            fury_width = int(self.fury_bar_width * fury_level)
            fury_rect = pygame.Rect(
                self.fury_bar_x, self.fury_bar_y + 6, fury_width, self.fury_bar_height
            )

            # Cor da barra baseada no nível
            if fury_level >= 1.0:
                color = (255, 0, 0)  # Vermelho quando cheia
            elif fury_level >= 0.5:
                color = (255, 165, 0)  # Laranja
            else:
                color = (255, 255, 0)  # Amarelo

            pygame.draw.rect(surface, color, fury_rect)

    def render_timer(self, surface):
        """Renderiza o contador de tempo"""
        current_time = pygame.time.get_ticks()
        elapsed_time = (
            current_time - self.start_time
        ) // 1000  # Converte para segundos

        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        time_text = f"{minutes:02d}:{seconds:02d}"
        text_surface = self.font.render(time_text, True, self.timer_color)

        # Posiciona o timer no canto superior direito
        timer_x = surface.get_width() - text_surface.get_width() - 20
        timer_y = 20

        surface.blit(text_surface, (timer_x, timer_y))

    def render(self, surface):
        """Renderiza todos os elementos da interface"""
        self.render_hearts(surface)
        self.render_jump_orb(surface)
        self.render_fury_bar(surface)
        self.render_timer(surface)

    def reset_timer(self):
        """Reseta o timer do jogo"""
        self.start_time = pygame.time.get_ticks()
