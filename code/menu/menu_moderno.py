# Menu moderno para o jogo
import pygame
import json
import os
from datetime import datetime


class MenuModerno:
    def __init__(self, screen):
        self.screen = screen
        self.largura, self.altura = screen.get_size()
        self.clock = pygame.time.Clock()
        self.running = True
        self.estado = "menu_principal"  # menu_principal, ranking, game_over, input_nome

        # Cores modernas
        self.cor_fundo = (15, 15, 25)
        self.cor_primaria = (100, 200, 255)
        self.cor_secundaria = (50, 150, 200)
        self.cor_texto = (255, 255, 255)
        self.cor_texto_secundario = (180, 180, 180)
        self.cor_botao = (40, 40, 60)
        self.cor_botao_hover = (60, 60, 80)
        self.cor_acento = (255, 100, 100)

        # Fontes
        try:
            self.fonte_titulo = pygame.font.Font(None, 72)
            self.fonte_subtitulo = pygame.font.Font(None, 36)
            self.fonte_botao = pygame.font.Font(None, 32)
            self.fonte_texto = pygame.font.Font(None, 24)
        except:
            self.fonte_titulo = pygame.font.SysFont("Arial", 72, bold=True)
            self.fonte_subtitulo = pygame.font.SysFont("Arial", 36)
            self.fonte_botao = pygame.font.SysFont("Arial", 32)
            self.fonte_texto = pygame.font.SysFont("Arial", 24)

        # Botões
        self.botoes = []
        self.botao_selecionado = 0

        # Sistema de ranking
        self.ranking_file = "data/ranking.json"
        self.ranking_data = self.carregar_ranking()

        # Input de nome
        self.nome_jogador = ""
        self.input_ativo = False

        # Animações
        self.tempo_animacao = 0

        # Callback para iniciar jogo
        self.callback_iniciar_jogo = None

        self.criar_botoes_menu_principal()

    def carregar_ranking(self):
        """Carrega o ranking do arquivo JSON"""
        try:
            if os.path.exists(self.ranking_file):
                with open(self.ranking_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # Cria diretório se não existir
                os.makedirs(os.path.dirname(self.ranking_file), exist_ok=True)
                return []
        except:
            return []

    def salvar_ranking(self):
        """Salva o ranking no arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.ranking_file), exist_ok=True)
            with open(self.ranking_file, "w", encoding="utf-8") as f:
                json.dump(self.ranking_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar ranking: {e}")

    def adicionar_ao_ranking(self, nome, tempo):
        """Adiciona um novo record ao ranking"""
        novo_record = {
            "nome": nome,
            "tempo": tempo,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }

        self.ranking_data.append(novo_record)
        # Ordena por tempo (menor primeiro), com fallback para distancia
        self.ranking_data.sort(key=lambda x: x.get("tempo", x.get("distancia", 0)))
        # Mantém apenas os 10 melhores
        self.ranking_data = self.ranking_data[:10]
        self.salvar_ranking()

    def criar_botoes_menu_principal(self):
        """Cria os botões do menu principal"""
        self.botoes = [
            {
                "texto": "JOGAR",
                "acao": self.ir_para_input_nome,
                "rect": pygame.Rect(self.largura // 2 - 100, 300, 200, 50),
            },
            {
                "texto": "RANKING",
                "acao": self.ir_para_ranking,
                "rect": pygame.Rect(self.largura // 2 - 100, 370, 200, 50),
            },
            {
                "texto": "SAIR",
                "acao": self.sair,
                "rect": pygame.Rect(self.largura // 2 - 100, 440, 200, 50),
            },
        ]

    def criar_botoes_ranking(self):
        """Cria os botões da tela de ranking"""
        self.botoes = [
            {
                "texto": "VOLTAR",
                "acao": self.voltar_menu_principal,
                "rect": pygame.Rect(self.largura // 2 - 100, 500, 200, 50),
            }
        ]

    def criar_botoes_game_over(self):
        """Cria os botões da tela de game over"""
        self.botoes = [
            {
                "texto": "JOGAR NOVAMENTE",
                "acao": self.reiniciar_jogo,
                "rect": pygame.Rect(self.largura // 2 - 120, 350, 240, 50),
            },
            {
                "texto": "MENU PRINCIPAL",
                "acao": self.voltar_menu_principal_game_over,
                "rect": pygame.Rect(self.largura // 2 - 120, 420, 240, 50),
            },
            {
                "texto": "SAIR",
                "acao": self.sair,
                "rect": pygame.Rect(self.largura // 2 - 120, 490, 240, 50),
            },
        ]

    def criar_botoes_input_nome(self):
        """Cria os botões da tela de input de nome"""
        self.botoes = [
            {
                "texto": "CONFIRMAR",
                "acao": self.confirmar_nome,
                "rect": pygame.Rect(self.largura // 2 - 100, 400, 200, 50),
            },
            {
                "texto": "VOLTAR",
                "acao": self.voltar_menu_principal,
                "rect": pygame.Rect(self.largura // 2 - 100, 470, 200, 50),
            },
        ]

    def ir_para_input_nome(self):
        self.estado = "input_nome"
        self.nome_jogador = ""
        self.input_ativo = True
        self.criar_botoes_input_nome()

    def ir_para_ranking(self):
        self.estado = "ranking"
        self.criar_botoes_ranking()

    def voltar_menu_principal(self):
        """Volta para o menu principal"""
        self.estado = "menu_principal"
        self.criar_botoes_menu_principal()
        # Não para o loop quando vem do ranking, apenas muda o estado
        # Só para o loop quando vem do game_over

    def voltar_menu_principal_game_over(self):
        """Volta para o menu principal a partir do game over"""
        self.estado = "menu_principal"
        self.criar_botoes_menu_principal()
        self.running = False  # Para o loop para retornar ao menu principal

    def confirmar_nome(self):
        if self.nome_jogador.strip():
            self.running = False
            return True
        return False

    def reiniciar_jogo(self):
        if self.callback_iniciar_jogo:
            self.callback_iniciar_jogo(self.nome_jogador)
        self.running = False

    def mostrar_game_over(self, tempo_jogo=None):
        """Mostra a tela de game over"""
        self.estado = "game_over"
        if tempo_jogo and self.nome_jogador:
            self.adicionar_ao_ranking(self.nome_jogador, tempo_jogo)
        self.criar_botoes_game_over()

    def sair(self):
        pygame.quit()
        exit()

    def desenhar_fundo_moderno(self):
        """Desenha um fundo moderno com gradiente"""
        # Gradiente vertical
        for y in range(self.altura):
            cor_r = int(15 + (y / self.altura) * 10)
            cor_g = int(15 + (y / self.altura) * 10)
            cor_b = int(25 + (y / self.altura) * 15)
            pygame.draw.line(
                self.screen, (cor_r, cor_g, cor_b), (0, y), (self.largura, y)
            )

        # Efeitos de partículas/estrelas
        import random

        for i in range(50):
            x = (i * 137 + self.tempo_animacao) % self.largura
            y = (i * 73 + self.tempo_animacao // 2) % self.altura
            alpha = int(
                100 + 50 * (0.5 + 0.5 * pygame.math.Vector2(x, y).length() / 100)
            )
            pygame.draw.circle(
                self.screen, (255, 255, 255, min(alpha, 255)), (int(x), int(y)), 1
            )

    def desenhar_botao(self, botao, index):
        """Desenha um botão moderno"""
        mouse_pos = pygame.mouse.get_pos()
        hover = botao["rect"].collidepoint(mouse_pos) or index == self.botao_selecionado

        # Cor do botão
        cor = self.cor_botao_hover if hover else self.cor_botao

        # Desenha sombra
        sombra_rect = botao["rect"].copy()
        sombra_rect.x += 3
        sombra_rect.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 100), sombra_rect, border_radius=10)

        # Desenha botão
        pygame.draw.rect(self.screen, cor, botao["rect"], border_radius=10)

        # Borda se hover
        if hover:
            pygame.draw.rect(
                self.screen, self.cor_primaria, botao["rect"], 2, border_radius=10
            )

        # Texto
        texto_surface = self.fonte_botao.render(botao["texto"], True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=botao["rect"].center)
        self.screen.blit(texto_surface, texto_rect)

    def desenhar_menu_principal(self):
        """Desenha o menu principal"""
        # Título
        titulo = self.fonte_titulo.render("JOGO SEM NOME", True, self.cor_primaria)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 150))
        self.screen.blit(titulo, titulo_rect)

        subtitulo = self.fonte_subtitulo.render(
            "NO MOMENTO", True, self.cor_texto_secundario
        )
        subtitulo_rect = subtitulo.get_rect(center=(self.largura // 2, 200))
        self.screen.blit(subtitulo, subtitulo_rect)

        # Botões
        for i, botao in enumerate(self.botoes):
            self.desenhar_botao(botao, i)

    def desenhar_ranking(self):
        """Desenha a tela de ranking"""
        # Título
        titulo = self.fonte_titulo.render("RANKING", True, self.cor_primaria)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 80))
        self.screen.blit(titulo, titulo_rect)

        # Lista de rankings
        y_start = 150
        for i, record in enumerate(self.ranking_data[:10]):
            y_pos = y_start + i * 30

            # Posição
            pos_text = self.fonte_texto.render(f"{i+1}.", True, self.cor_acento)
            self.screen.blit(pos_text, (100, y_pos))

            # Nome
            nome_text = self.fonte_texto.render(record["nome"], True, self.cor_texto)
            self.screen.blit(nome_text, (140, y_pos))

            # Tempo ou Distância (compatibilidade com formato antigo)
            if "tempo" in record:
                minutos = record["tempo"] // 60
                segundos = record["tempo"] % 60
                tempo_text = self.fonte_texto.render(
                    f"{minutos:02d}:{segundos:02d}", True, self.cor_texto_secundario
                )
            elif "distancia" in record:
                tempo_text = self.fonte_texto.render(
                    f"Dist: {record['distancia']}", True, self.cor_texto_secundario
                )
            else:
                tempo_text = self.fonte_texto.render(
                    "--:--", True, self.cor_texto_secundario
                )
            self.screen.blit(tempo_text, (400, y_pos))

            # Data
            if "data" in record:
                data_text = self.fonte_texto.render(
                    record["data"], True, self.cor_texto_secundario
                )
                self.screen.blit(data_text, (500, y_pos))
            else:
                data_text = self.fonte_texto.render(
                    "--/--/----", True, self.cor_texto_secundario
                )
                self.screen.blit(data_text, (500, y_pos))

        if not self.ranking_data:
            texto = self.fonte_subtitulo.render(
                "Nenhum record ainda!", True, self.cor_texto_secundario
            )
            texto_rect = texto.get_rect(center=(self.largura // 2, 300))
            self.screen.blit(texto, texto_rect)

        # Botões
        for i, botao in enumerate(self.botoes):
            self.desenhar_botao(botao, i)

    def desenhar_input_nome(self):
        """Desenha a tela de input de nome"""
        # Título
        titulo = self.fonte_titulo.render("DIGITE SEU NOME", True, self.cor_primaria)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 200))
        self.screen.blit(titulo, titulo_rect)

        # Campo de input
        input_rect = pygame.Rect(self.largura // 2 - 150, 300, 300, 50)
        cor_input = self.cor_botao_hover if self.input_ativo else self.cor_botao
        pygame.draw.rect(self.screen, cor_input, input_rect, border_radius=10)

        if self.input_ativo:
            pygame.draw.rect(
                self.screen, self.cor_primaria, input_rect, 2, border_radius=10
            )

        # Texto do input
        texto_input = self.nome_jogador + (
            "_" if self.input_ativo and (self.tempo_animacao // 30) % 2 else ""
        )
        if not texto_input.replace("_", ""):
            texto_input = "Digite aqui..."
            cor_texto = self.cor_texto_secundario
        else:
            cor_texto = self.cor_texto

        texto_surface = self.fonte_botao.render(texto_input, True, cor_texto)
        texto_rect = texto_surface.get_rect(center=input_rect.center)
        self.screen.blit(texto_surface, texto_rect)

        # Botões
        for i, botao in enumerate(self.botoes):
            self.desenhar_botao(botao, i)

    def desenhar_game_over(self):
        """Desenha a tela de game over"""
        # Título
        titulo = self.fonte_titulo.render("GAME OVER", True, self.cor_acento)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 200))
        self.screen.blit(titulo, titulo_rect)

        # Mensagem
        if self.nome_jogador:
            msg = self.fonte_subtitulo.render(
                f"Boa tentativa, {self.nome_jogador}!", True, self.cor_texto
            )
            msg_rect = msg.get_rect(center=(self.largura // 2, 260))
            self.screen.blit(msg, msg_rect)

        # Botões
        for i, botao in enumerate(self.botoes):
            self.desenhar_botao(botao, i)

    def processar_eventos(self):
        """Processa os eventos do menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sair()

            elif event.type == pygame.KEYDOWN:
                if self.estado == "input_nome" and self.input_ativo:
                    if event.key == pygame.K_RETURN:
                        if self.confirmar_nome():
                            return self.nome_jogador.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        self.nome_jogador = self.nome_jogador[:-1]
                    elif event.unicode.isprintable() and len(self.nome_jogador) < 20:
                        self.nome_jogador += event.unicode

                elif event.key == pygame.K_UP:
                    self.botao_selecionado = (self.botao_selecionado - 1) % len(
                        self.botoes
                    )
                elif event.key == pygame.K_DOWN:
                    self.botao_selecionado = (self.botao_selecionado + 1) % len(
                        self.botoes
                    )
                elif event.key == pygame.K_RETURN:
                    if self.botoes:
                        botao = self.botoes[self.botao_selecionado]
                        if (
                            botao["texto"] == "CONFIRMAR"
                            and self.estado == "input_nome"
                        ):
                            if self.confirmar_nome():
                                return self.nome_jogador.strip()
                        else:
                            botao["acao"]()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo
                    mouse_pos = pygame.mouse.get_pos()

                    if self.estado == "input_nome":
                        input_rect = pygame.Rect(self.largura // 2 - 150, 300, 300, 50)
                        self.input_ativo = input_rect.collidepoint(mouse_pos)

                    for i, botao in enumerate(self.botoes):
                        if botao["rect"].collidepoint(mouse_pos):
                            self.botao_selecionado = i
                            if (
                                botao["texto"] == "CONFIRMAR"
                                and self.estado == "input_nome"
                            ):
                                if self.confirmar_nome():
                                    return self.nome_jogador.strip()
                            else:
                                botao["acao"]()
                            break
        return None

    def run(self):
        """Loop principal do menu"""
        print(f"Menu iniciado - Estado: {self.estado}")
        while self.running:
            self.tempo_animacao += 1

            result = self.processar_eventos()
            if result:  # Se processar_eventos retornou algo
                print(f"Menu retornando: {result}")
                return result

            # Desenha
            self.desenhar_fundo_moderno()

            if self.estado == "menu_principal":
                self.desenhar_menu_principal()
            elif self.estado == "ranking":
                self.desenhar_ranking()
            elif self.estado == "input_nome":
                self.desenhar_input_nome()
            elif self.estado == "game_over":
                self.desenhar_game_over()

            pygame.display.flip()
            self.clock.tick(60)

        print(f"Menu finalizado - Nome: {self.nome_jogador}")
        return self.nome_jogador if self.nome_jogador else None
