# Menu moderno para o jogo
import pygame
import json
import os
import math
import random
from datetime import datetime


class MenuModerno:
    def __init__(self, screen, callback_iniciar_jogo=None):
        """Inicializa o menu moderno"""
        pygame.init()
        self.__screen = screen
        self.__largura, self.__altura = screen.get_size()
        self.__clock = pygame.time.Clock()

        # Estados
        self.running = True
        self.estado = "menu_principal"  # menu_principal, ranking, input_nome, game_over

        # Esquema de cores moderno
        self.__cor_primaria = (64, 224, 208)  # Turquesa
        self.__cor_acento = (255, 99, 71)  # Coral
        self.__cor_base = (25, 25, 35)  # Azul escuro
        self.__cor_botao = (45, 45, 60)
        self.__cor_botao_hover = (65, 65, 85)
        self.__cor_texto = (240, 240, 240)
        self.__cor_texto_secundario = (180, 180, 180)

        # Fontes
        try:
            self.__fonte_titulo = pygame.font.Font("assets/fonts/PixelifySans.ttf", 48)
            self.__fonte_subtitulo = pygame.font.Font(
                "assets/fonts/PixelifySans.ttf", 24
            )
            self.__fonte_botao = pygame.font.Font("assets/fonts/PixelifySans.ttf", 20)
            self.__fonte_texto = pygame.font.Font("assets/fonts/PixelifySans.ttf", 18)
            self.__fonte_texto = pygame.font.Font("assets/fonts/PixelifySans.ttf", 18)
            raise FileNotFoundError("Font file not found or invalid")
        except:
            # Fallback para fontes do sistema
            self.__fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)
            self.__fonte_subtitulo = pygame.font.SysFont("Arial", 24)
            self.__fonte_botao = pygame.font.SysFont("Arial", 20, bold=True)
            self.__fonte_texto = pygame.font.SysFont("Arial", 18)

        # Sistema de botões
        self.__botoes = []
        self.__botao_selecionado = 0

        # Sistema de ranking
        self.__ranking_file = "data/ranking.json"
        self.__ranking_data = []
        self.carregar_ranking()

        # Input de nome do jogador
        self.__nome_jogador = ""
        self.__input_ativo = False

        # Animações
        self.__tempo_animacao = 0

        # Callback para iniciar jogo
        self.callback_iniciar_jogo = callback_iniciar_jogo

        # Inicializa com menu principal
        self.criar_botoes_menu_principal()

    def carregar_ranking(self):
        """Carrega o ranking do arquivo JSON"""
        try:
            if os.path.exists(self.__ranking_file):
                with open(self.__ranking_file, "r", encoding="utf-8") as f:
                    self.__ranking_data = json.load(f)
            else:
                # Cria diretório se não existir
                os.makedirs(os.path.dirname(self.__ranking_file), exist_ok=True)
                self.__ranking_data = []
        except:
            self.__ranking_data = []

    def salvar_ranking(self):
        """Salva o ranking no arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.__ranking_file), exist_ok=True)
            with open(self.__ranking_file, "w", encoding="utf-8") as f:
                json.dump(self.__ranking_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar ranking: {e}")

    def adicionar_ao_ranking(self, nome, tempo):
        """Adiciona um novo record ao ranking"""
        agora = datetime.now()
        novo_record = {
            "nome": nome,
            "tempo": tempo,
            "data": agora.strftime("%d/%m/%Y"),
            "hora": agora.strftime("%H:%M:%S")
        }
        
        # Verifica se já existe um registro idêntico
        for record in self.__ranking_data:
            if (record.get("nome") == nome and 
                record.get("tempo") == tempo and 
                record.get("data") == novo_record["data"]):
                return  # Não adiciona se já existir um registro idêntico
        
        # Adiciona o novo record à lista
        self.__ranking_data.append(novo_record)
        
        # Ordena por tempo (menor é melhor), tratando registros antigos com 'distancia'
        self.__ranking_data.sort(
            key=lambda x: x.get("tempo", x.get("distancia", float("inf")))
        )
        # Mantém apenas os 10 melhores
        self.__ranking_data = self.__ranking_data[:10]
        self.salvar_ranking()

    def criar_botoes_menu_principal(self):
        """Cria os botões do menu principal"""
        self.__botoes = [
            {
                "texto": "JOGAR",
                "acao": self.ir_para_input_nome,
                "rect": pygame.Rect(self.__largura // 2 - 100, 280, 200, 50),
            },
            {
                "texto": "RANKING",
                "acao": self.ir_para_ranking,
                "rect": pygame.Rect(self.__largura // 2 - 100, 350, 200, 50),
            },
            {
                "texto": "SAIR",
                "acao": self.sair,
                "rect": pygame.Rect(self.__largura // 2 - 100, 420, 200, 50),
            },
        ]

    def criar_botoes_ranking(self):
        """Cria os botões da tela de ranking"""
        self.__botoes = [
            {
                "texto": "VOLTAR",
                "acao": self.voltar_menu_principal,
                "rect": pygame.Rect(self.__largura // 2 - 100, 500, 200, 50),
            }
        ]

    def criar_botoes_game_over(self):
        """Cria os botões da tela de game over"""
        self.__botoes = [
            {
                "texto": "JOGAR NOVAMENTE",
                "acao": self.reiniciar_jogo,
                "rect": pygame.Rect(self.__largura // 2 - 120, 350, 240, 50),
            },
            {
                "texto": "MENU PRINCIPAL",
                "acao": self.voltar_menu_principal_game_over,
                "rect": pygame.Rect(self.__largura // 2 - 120, 420, 240, 50),
            },
            {
                "texto": "SAIR",
                "acao": self.sair,
                "rect": pygame.Rect(self.__largura // 2 - 120, 490, 240, 50),
            },
        ]

    def criar_botoes_input_nome(self):
        """Cria os botões da tela de input de nome"""
        self.__botoes = [
            {
                "texto": "CONFIRMAR",
                "acao": self.confirmar_nome,
                "rect": pygame.Rect(self.__largura // 2 - 100, 400, 200, 50),
            },
            {
                "texto": "VOLTAR",
                "acao": self.voltar_menu_principal,
                "rect": pygame.Rect(self.__largura // 2 - 100, 470, 200, 50),
            },
        ]

    def ir_para_input_nome(self):
        """Vai para a tela de input de nome"""
        self.estado = "input_nome"
        self.__nome_jogador = ""
        self.__input_ativo = True
        self.__botao_selecionado = 0
        self.criar_botoes_input_nome()

    def ir_para_ranking(self):
        """Vai para a tela de ranking"""
        self.estado = "ranking"
        self.__botao_selecionado = 0
        self.criar_botoes_ranking()

    def voltar_menu_principal(self):
        """Volta para o menu principal"""
        self.estado = "menu_principal"
        self.__botao_selecionado = 0
        self.criar_botoes_menu_principal()

    def voltar_menu_principal_game_over(self):
        """Volta para o menu principal a partir do game over"""
        self.estado = "menu_principal"
        self.__botao_selecionado = 0
        self.criar_botoes_menu_principal()
        self.running = False

    def confirmar_nome(self):
        """Confirma o nome do jogador e inicia o jogo"""
        if self.__nome_jogador.strip():
            return self.__nome_jogador.strip()

    def reiniciar_jogo(self):
        """Reinicia o jogo"""
        if self.callback_iniciar_jogo:
            self.callback_iniciar_jogo(self.__nome_jogador)
        return self.__nome_jogador.strip()

    def mostrar_game_over(self, tempo_jogo=None):
        """Mostra a tela de game over"""
        # O ranking será adicionado na tela de vitória, não no game over
        self.estado = "game_over"
        self.__botao_selecionado = 0
        self.criar_botoes_game_over()

    def sair(self):
        """Sai do jogo"""
        self.running = False

    def desenhar_fundo_gradiente(self):
        """Desenha um fundo com gradiente"""
        for y in range(self.__altura):
            cor_r = int(15 + (y / self.__altura) * 10)
            cor_g = int(15 + (y / self.__altura) * 10)
            cor_b = int(25 + (y / self.__altura) * 15)
            pygame.draw.line(
                self.__screen, (cor_r, cor_g, cor_b), (0, y), (self.__largura, y)
            )

    def desenhar_particulas(self):
        """Desenha partículas animadas no fundo"""
        for i in range(20):
            x = (i * 137 + self.__tempo_animacao) % self.__largura
            y = (i * 73 + self.__tempo_animacao // 2) % self.__altura
            alpha = 50 + 30 * (i % 3)
            if alpha > 255:
                alpha = 255
            pygame.draw.circle(
                self.__screen, (255, 255, 255, min(alpha, 255)), (int(x), int(y)), 1
            )

    def desenhar_botao(self, botao, index, mouse_pos):
        """Desenha um botão com efeitos visuais"""
        hover = (
            botao["rect"].collidepoint(mouse_pos) or index == self.__botao_selecionado
        )

        # Cor do botão
        cor = self.__cor_botao_hover if hover else self.__cor_botao

        # Sombra
        sombra_rect = botao["rect"].copy()
        sombra_rect.x += 3
        sombra_rect.y += 3
        pygame.draw.rect(self.__screen, (0, 0, 0, 100), sombra_rect, border_radius=10)

        # Botão principal
        pygame.draw.rect(self.__screen, cor, botao["rect"], border_radius=10)

        # Borda se selecionado
        if hover:
            pygame.draw.rect(
                self.__screen, self.__cor_primaria, botao["rect"], 2, border_radius=10
            )

        # Texto
        texto_surface = self.__fonte_botao.render(
            botao["texto"], True, self.__cor_texto
        )
        texto_rect = texto_surface.get_rect(center=botao["rect"].center)
        self.__screen.blit(texto_surface, texto_rect)

    def desenhar_menu_principal(self, mouse_pos):
        """Desenha o menu principal"""
        titulo = self.__fonte_titulo.render("JOGO SEM NOME", True, self.__cor_primaria)
        titulo_rect = titulo.get_rect(center=(self.__largura // 2, 150))
        self.__screen.blit(titulo, titulo_rect)

        subtitulo = self.__fonte_subtitulo.render(
            "NO MOMENTO", True, self.__cor_texto_secundario
        )
        subtitulo_rect = subtitulo.get_rect(center=(self.__largura // 2, 200))
        self.__screen.blit(subtitulo, subtitulo_rect)

        # Desenha botões
        for i, botao in enumerate(self.__botoes):
            self.desenhar_botao(botao, i, mouse_pos)

    def desenhar_ranking(self, mouse_pos):
        """Desenha a tela de ranking"""
        titulo = self.__fonte_titulo.render("RANKING", True, self.__cor_primaria)
        titulo_rect = titulo.get_rect(center=(self.__largura // 2, 80))
        self.__screen.blit(titulo, titulo_rect)

        # Cabeçalhos das colunas
        cabecalho_y = 130
        pos_header = self.__fonte_texto.render("#", True, self.__cor_acento)
        self.__screen.blit(pos_header, (100, cabecalho_y))
        
        nome_header = self.__fonte_texto.render("NOME", True, self.__cor_acento)
        self.__screen.blit(nome_header, (140, cabecalho_y))
        
        tempo_header = self.__fonte_texto.render("TEMPO", True, self.__cor_acento)
        self.__screen.blit(tempo_header, (320, cabecalho_y))
        
        data_header = self.__fonte_texto.render("DATA", True, self.__cor_acento)
        self.__screen.blit(data_header, (420, cabecalho_y))
        
        hora_header = self.__fonte_texto.render("HORA", True, self.__cor_acento)
        self.__screen.blit(hora_header, (520, cabecalho_y))

        # Lista os records
        y_start = 160
        for i, record in enumerate(self.__ranking_data[:10]):
            y_pos = y_start + i * 30

            # Posição
            pos_text = self.__fonte_texto.render(f"{i+1}.", True, self.__cor_acento)
            self.__screen.blit(pos_text, (100, y_pos))

            # Nome (limitado a 12 caracteres)
            nome_display = record["nome"][:12] + "..." if len(record["nome"]) > 12 else record["nome"]
            nome_text = self.__fonte_texto.render(
                nome_display, True, self.__cor_texto
            )
            self.__screen.blit(nome_text, (140, y_pos))

            # Tempo
            if "tempo" in record:
                tempo_segundos = record["tempo"]
                minutos = tempo_segundos // 60
                segundos = tempo_segundos % 60
                tempo_text = self.__fonte_texto.render(
                    f"{minutos:02d}:{segundos:02d}", True, self.__cor_texto_secundario
                )
            elif "distancia" in record:
                tempo_text = self.__fonte_texto.render(
                    f"{record['distancia']}", True, self.__cor_texto_secundario
                )
            else:
                tempo_text = self.__fonte_texto.render(
                    "--:--", True, self.__cor_texto_secundario
                )
            self.__screen.blit(tempo_text, (320, y_pos))

            # Data
            if "data" in record:
                data_text = self.__fonte_texto.render(
                    record["data"], True, self.__cor_texto_secundario
                )
            else:
                data_text = self.__fonte_texto.render(
                    "--/--/--", True, self.__cor_texto_secundario
                )
            self.__screen.blit(data_text, (420, y_pos))
            
            # Hora
            if "hora" in record:
                hora_text = self.__fonte_texto.render(
                    record["hora"], True, self.__cor_texto_secundario
                )
            else:
                hora_text = self.__fonte_texto.render(
                    "--:--:--", True, self.__cor_texto_secundario
                )
            self.__screen.blit(hora_text, (520, y_pos))

        if not self.__ranking_data:
            texto = self.__fonte_subtitulo.render(
                "Nenhum record ainda!", True, self.__cor_texto_secundario
            )
            texto_rect = texto.get_rect(center=(self.__largura // 2, 300))
            self.__screen.blit(texto, texto_rect)

        # Desenha botões
        for i, botao in enumerate(self.__botoes):
            self.desenhar_botao(botao, i, mouse_pos)

    def desenhar_input_nome(self, mouse_pos):
        """Desenha a tela de input de nome"""
        titulo = self.__fonte_titulo.render(
            "DIGITE SEU NOME", True, self.__cor_primaria
        )
        titulo_rect = titulo.get_rect(center=(self.__largura // 2, 200))
        self.__screen.blit(titulo, titulo_rect)

        # Campo de input
        input_rect = pygame.Rect(self.__largura // 2 - 150, 300, 300, 50)
        cor_input = self.__cor_botao_hover if self.__input_ativo else self.__cor_botao
        pygame.draw.rect(self.__screen, cor_input, input_rect, border_radius=10)

        if self.__input_ativo:
            pygame.draw.rect(
                self.__screen, self.__cor_primaria, input_rect, 2, border_radius=10
            )

        # Texto do input com cursor piscando
        texto_input = self.__nome_jogador + (
            "_" if self.__input_ativo and (self.__tempo_animacao // 30) % 2 else ""
        )

        # Cor do texto baseada no estado
        if not self.__nome_jogador.strip():
            cor_texto = self.__cor_texto_secundario
        else:
            cor_texto = self.__cor_texto

        texto_surface = self.__fonte_botao.render(texto_input, True, cor_texto)
        texto_rect = texto_surface.get_rect(center=input_rect.center)
        self.__screen.blit(texto_surface, texto_rect)

        # Desenha botões
        for i, botao in enumerate(self.__botoes):
            self.desenhar_botao(botao, i, mouse_pos)

    def desenhar_game_over(self, mouse_pos):
        """Desenha a tela de game over"""
        titulo = self.__fonte_titulo.render("GAME OVER", True, self.__cor_acento)
        titulo_rect = titulo.get_rect(center=(self.__largura // 2, 200))
        self.__screen.blit(titulo, titulo_rect)

        # Mensagem personalizada
        if self.__nome_jogador:
            msg = self.__fonte_subtitulo.render(
                f"Boa tentativa, {self.__nome_jogador}!", True, self.__cor_texto
            )
            msg_rect = msg.get_rect(center=(self.__largura // 2, 260))
            self.__screen.blit(msg, msg_rect)

        # Desenha botões
        for i, botao in enumerate(self.__botoes):
            self.desenhar_botao(botao, i, mouse_pos)

    def processar_input_teclado(self, event):
        """Processa input do teclado"""
        if event.type == pygame.KEYDOWN:
            if self.estado == "input_nome" and self.__input_ativo:
                if event.key == pygame.K_RETURN:
                    return self.__nome_jogador.strip()
                elif event.key == pygame.K_BACKSPACE:
                    self.__nome_jogador = self.__nome_jogador[:-1]
                elif event.unicode.isprintable() and len(self.__nome_jogador) < 20:
                    self.__nome_jogador += event.unicode
            else:
                if event.key == pygame.K_UP:
                    self.__botao_selecionado = (self.__botao_selecionado - 1) % len(
                        self.__botoes
                    )
                elif event.key == pygame.K_DOWN:
                    self.__botao_selecionado = (self.__botao_selecionado + 1) % len(
                        self.__botoes
                    )
                elif event.key == pygame.K_RETURN:
                    if self.__botoes:
                        botao = self.__botoes[self.__botao_selecionado]
                        if botao["acao"]:
                            resultado = botao["acao"]()
                            if resultado:
                                return resultado
                    return self.__nome_jogador.strip()
        return None

    def processar_input_mouse(self, event, mouse_pos):
        """Processa input do mouse"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.estado == "input_nome":
                input_rect = pygame.Rect(self.__largura // 2 - 150, 300, 300, 50)
                self.__input_ativo = input_rect.collidepoint(mouse_pos)

            for i, botao in enumerate(self.__botoes):
                if botao["rect"].collidepoint(mouse_pos):
                    self.__botao_selecionado = i
                    if botao["acao"]:
                        resultado = botao["acao"]()
                        if resultado:
                            return resultado
                    return self.__nome_jogador.strip()
        elif event.type == pygame.MOUSEMOTION:
            for i, botao in enumerate(self.__botoes):
                if botao["rect"].collidepoint(mouse_pos):
                    self.__botao_selecionado = i
                    break
        return None

    def run(self):
        """Loop principal do menu"""
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            self.__tempo_animacao += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None

                resultado = self.processar_input_teclado(event)
                if resultado:
                    return resultado

                resultado = self.processar_input_mouse(event, mouse_pos)
                if resultado:
                    return resultado

            # Desenha tudo
            self.desenhar_fundo_gradiente()
            self.desenhar_particulas()

            if self.estado == "menu_principal":
                self.desenhar_menu_principal(mouse_pos)
            elif self.estado == "ranking":
                self.desenhar_ranking(mouse_pos)
            elif self.estado == "input_nome":
                self.desenhar_input_nome(mouse_pos)
            elif self.estado == "game_over":
                self.desenhar_game_over(mouse_pos)

            pygame.display.flip()
            self.__clock.tick(60)

        print(f"Menu finalizado - Nome: {self.__nome_jogador}")
        return self.__nome_jogador if self.__nome_jogador else None
