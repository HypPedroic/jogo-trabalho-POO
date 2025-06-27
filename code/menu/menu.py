# Menu moderno para o jogo
import pygame
import json
import os
import math
import random
from datetime import datetime


class Menu:
    def __init__(self, screen, callback_iniciar_jogo=None):
        """Inicializa o menu moderno"""
        pygame.init()
        self.__screen = screen
        self.__largura, self.__altura = screen.get_size()
        self.__clock = pygame.time.Clock()

        # Estados
        self.__running = True
        self.__estado = "menu_principal"  # menu_principal, ranking, input_nome, game_over
        
        # Sistema de dificuldade
        self.__dificuldades = ["FÁCIL", "NORMAL", "DIFÍCIL"]
        self.__cores_dificuldade = {
            "FÁCIL": (0, 255, 0),  # Verde
            "NORMAL": (255, 255, 0),  # Amarelo
            "DIFÍCIL": (255, 0, 0)  # Vermelho
        }
        self.__dificuldade_atual = "NORMAL"
        self.__inimigos_por_dificuldade = {
            "FÁCIL": 5,
            "NORMAL": 15,
            "DIFÍCIL": 30
        }

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
        self.__callback_iniciar_jogo = callback_iniciar_jogo

        # Inicializa com menu principal
        self.criar_botoes_menu_principal()
        
    @property
    def botoes(self):
        return self.__botoes

    @botoes.setter
    def botoes(self, value):
        self.__botoes = value

    @property
    def botao_selecionado(self):
        return self.__botao_selecionado

    @botao_selecionado.setter
    def botao_selecionado(self, value):
        self.__botao_selecionado = value

    @property
    def nome_jogador(self):
        return self.__nome_jogador

    @nome_jogador.setter
    def nome_jogador(self, value):
        self.__nome_jogador = value

    @property
    def input_ativo(self):
        return self.__input_ativo

    @input_ativo.setter
    def input_ativo(self, value):
        self.__input_ativo = value

    @property
    def dificuldade_atual(self):
        return self.__dificuldade_atual

    @dificuldade_atual.setter
    def dificuldade_atual(self, value):
        self.__dificuldade_atual = value

    @property
    def inimigos_por_dificuldade(self):
        return self.__inimigos_por_dificuldade

    @inimigos_por_dificuldade.setter
    def inimigos_por_dificuldade(self, value):
        self.__inimigos_por_dificuldade = value

    @property
    def ranking_data(self):
        return self.__ranking_data

    @ranking_data.setter
    def ranking_data(self, value):
        self.__ranking_data = value

    @property
    def largura(self):
        return self.__largura
    
    @largura.setter
    def largura(self, valor):
        self.__largura = valor

    @property
    def altura(self):
        return self.__altura
    
    @altura.setter
    def altura(self, valor):
        self.__altura = valor

    @property
    def tempo_animacao(self):
        return self.__tempo_animacao

    @tempo_animacao.setter
    def tempo_animacao(self, value):
        self.__tempo_animacao = value

    @property
    def clock(self):
        return self.__clock
    
    @clock.setter
    def clock(self, valor):
        self.__clock = valor
        
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
    def screen(self):
        return self.__screen

    @property
    def dificuldades(self):
        return self.__dificuldades

    @property
    def cores_dificuldade(self):
        return self.__cores_dificuldade

    @property
    def callback_iniciar_jogo(self):
        return self.__callback_iniciar_jogo

    @callback_iniciar_jogo.setter
    def callback_iniciar_jogo(self, value):
        self.__callback_iniciar_jogo = value 
        
    @property
    def cor_primaria(self):
        return self.__cor_primaria

    @cor_primaria.setter
    def cor_primaria(self, value):
        self.__cor_primaria = value

    @property
    def cor_acento(self):
        return self.__cor_acento

    @cor_acento.setter
    def cor_acento(self, value):
        self.__cor_acento = value

    @property
    def cor_base(self):
        return self.__cor_base

    @cor_base.setter
    def cor_base(self, value):
        self.__cor_base = value

    @property
    def cor_botao(self):
        return self.__cor_botao

    @cor_botao.setter
    def cor_botao(self, value):
        self.__cor_botao = value

    @property
    def cor_botao_hover(self):
        return self.__cor_botao_hover

    @cor_botao_hover.setter
    def cor_botao_hover(self, value):
        self.__cor_botao_hover = value

    @property
    def cor_texto(self):
        return self.__cor_texto

    @cor_texto.setter
    def cor_texto(self, value):
        self.__cor_texto = value

    @property
    def cor_texto_secundario(self):
        return self.__cor_texto_secundario

    @cor_texto_secundario.setter
    def cor_texto_secundario(self, value):
        self.__cor_texto_secundario = value

    @property
    def fonte_titulo(self):
        return self.__fonte_titulo

    @fonte_titulo.setter
    def fonte_titulo(self, value):
        self.__fonte_titulo = value

    @property
    def fonte_subtitulo(self):
        return self.__fonte_subtitulo

    @fonte_subtitulo.setter
    def fonte_subtitulo(self, value):
        self.__fonte_subtitulo = value

    @property
    def fonte_botao(self):
        return self.__fonte_botao

    @fonte_botao.setter
    def fonte_botao(self, value):
        self.__fonte_botao = value

    @property
    def fonte_texto(self):
        return self.__fonte_texto

    @fonte_texto.setter
    def fonte_texto(self, value):
        self.__fonte_texto = value

    @property
    def ranking_file(self):
        return self.__ranking_file

    @ranking_file.setter
    def ranking_file(self, value):
        self.__ranking_file = value

    @property
    def tempo_jogo(self):
        return getattr(self, '_Menu__tempo_jogo', None)

    @tempo_jogo.setter
    def tempo_jogo(self, value):
        self.__tempo_jogo = value

    @property
    def inimigos_mortos(self):
        return getattr(self, '_Menu__inimigos_mortos', None)

    @inimigos_mortos.setter
    def inimigos_mortos(self, value):
        self.__inimigos_mortos = value

    @property
    def total_inimigos(self):
        return getattr(self, '_Menu__total_inimigos', None)

    @total_inimigos.setter
    def total_inimigos(self, value):
        self.__total_inimigos = value

    @property
    def vida_restante(self):
        return getattr(self, '_Menu__vida_restante', None)

    @vida_restante.setter
    def vida_restante(self, value):
        self.__vida_restante = value

    @property
    def vida_maxima(self):
        return getattr(self, '_Menu__vida_maxima', None)

    @vida_maxima.setter
    def vida_maxima(self, value):
        self.__vida_maxima = value 

    def carregar_ranking(self):
        """Carrega o ranking do arquivo JSON"""
        try:
            if os.path.exists(self.ranking_file):
                with open(self.ranking_file, "r", encoding="utf-8") as f:
                    self.ranking_data = json.load(f)
            else:
                # Cria diretório se não existir
                os.makedirs(os.path.dirname(self.ranking_file), exist_ok=True)
                self.ranking_data = []
        except:
            self.ranking_data = []

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
        agora = datetime.now()
        novo_record = {
            "nome": nome,
            "tempo": tempo,
            "data": agora.strftime("%d/%m/%Y"),
            "hora": agora.strftime("%H:%M:%S")
        }
        
        # Verifica se já existe um registro idêntico
        for record in self.ranking_data:
            if (record.get("nome") == nome and 
                record.get("tempo") == tempo and 
                record.get("data") == novo_record["data"]):
                return  # Não adiciona se já existir um registro idêntico
        
        # Adiciona o novo record à lista
        self.ranking_data.append(novo_record)
        
        # Ordena por tempo (menor é melhor), tratando registros antigos com 'distancia'
        self.ranking_data.sort(
            key=lambda x: x.get("tempo", x.get("distancia", float("inf")))
        )
        # Mantém apenas os 10 melhores
        self.ranking_data = self.ranking_data[:10]
        self.salvar_ranking()

    def existe_save(self):
        return os.path.exists("data/save.json")

    def criar_botoes_menu_principal(self):
        self.botoes = []
        if self.existe_save():
            self.botoes.append({
                "texto": "CONTINUAR PARTIDA",
                "acao": self.continuar_partida,
                "rect": pygame.Rect(self.largura // 2 - 100, 210, 200, 50),
            })
        self.botoes.extend([
            {
                "texto": "JOGAR",
                "acao": self.ir_para_input_nome,
                "rect": pygame.Rect(self.largura // 2 - 100, 280, 200, 50),
            },
            {
                "texto": "RANKING",
                "acao": self.ir_para_ranking,
                "rect": pygame.Rect(self.largura // 2 - 100, 350, 200, 50),
            },
            {
                "texto": "SAIR",
                "acao": self.sair,
                "rect": pygame.Rect(self.largura // 2 - 100, 420, 200, 50),
            },
        ])

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
                "texto": "MENU PRINCIPAL",
                "acao": self.voltar_menu_principal_game_over,
                "rect": pygame.Rect(self.largura // 2 - 120, 350, 240, 50),
            },
            {
                "texto": "SAIR",
                "acao": self.sair,
                "rect": pygame.Rect(self.largura // 2 - 120, 420, 240, 50),
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
        """Vai para a tela de input de nome"""
        self.estado = "input_nome"
        self.nome_jogador = ""
        self.input_ativo = True
        self.botao_selecionado = 0
        self.criar_botoes_input_nome()

    def ir_para_ranking(self):
        """Vai para a tela de ranking"""
        self.estado = "ranking"
        self.botao_selecionado = 0
        self.criar_botoes_ranking()

    def voltar_menu_principal(self):
        """Volta para o menu principal"""
        self.estado = "menu_principal"
        self.botao_selecionado = 0
        self.criar_botoes_menu_principal()

    def voltar_menu_principal_game_over(self):
        """Volta para o menu principal a partir do game over"""
        self.estado = "menu_principal"
        self.nome_jogador = ""
        self.botao_selecionado = 0
        self.criar_botoes_menu_principal()
        self.running = False

    def confirmar_nome(self):
        """Confirma o nome do jogador e inicia o jogo"""
        if self.nome_jogador.strip():
            return {
                "nome": self.nome_jogador.strip(),
                "dificuldade": self.dificuldade_atual,
                "num_inimigos": self.inimigos_por_dificuldade[self.dificuldade_atual]
            }
        return False

    def reiniciar_jogo(self):
        """Reinicia o jogo com o mesmo nome do jogador"""
        if self.callback_iniciar_jogo and self.nome_jogador.strip():
            self.callback_iniciar_jogo({
                "nome": self.nome_jogador.strip(),
                "dificuldade": self.dificuldade_atual,
                "num_inimigos": self.inimigos_por_dificuldade[self.dificuldade_atual]
            })
            return True
        return False

    def mostrar_game_over(self, tempo_jogo=None):
        """Mostra a tela de game over"""
        # O ranking será adicionado na tela de vitória, não no game over
        self.estado = "game_over"
        self.botao_selecionado = 0
        self.criar_botoes_game_over()

    def criar_botoes_vitoria(self):
        """Cria os botões da tela de vitória"""
        self.botoes = [
            {
                "texto": "MENU PRINCIPAL",
                "acao": self.voltar_menu_principal_game_over,
                "rect": pygame.Rect(self.largura // 2 - 120, 350, 240, 50),
            },
            {
                "texto": "SAIR",
                "acao": self.sair,
                "rect": pygame.Rect(self.largura // 2 - 120, 420, 240, 50),
            },
        ]

    def mostrar_vitoria(self, tempo_jogo, estatisticas):
        """Mostra a tela de vitória com estatísticas"""
        self.estado = "vitoria"
        self.botao_selecionado = 0
        self.criar_botoes_vitoria()
        
        # Armazena as estatísticas para exibição
        self.tempo_jogo = tempo_jogo
        self.inimigos_mortos = estatisticas.get('inimigos_mortos', 0)
        self.total_inimigos = estatisticas.get('total_inimigos', 0)
        self.vida_restante = estatisticas.get('vida_restante', 0)
        self.vida_maxima = estatisticas.get('vida_maxima', 0)
        
        if tempo_jogo is not None and self.nome_jogador:
            self.adicionar_ao_ranking(self.nome_jogador, tempo_jogo)

    def sair(self):
        """Sai do jogo"""
        self.running = False

    def continuar_partida(self):
        return "continuar"

    def desenhar_fundo_gradiente(self):
        """Desenha um fundo com gradiente"""
        for y in range(self.altura):
            cor_r = int(15 + (y / self.altura) * 10)
            cor_g = int(15 + (y / self.altura) * 10)
            cor_b = int(25 + (y / self.altura) * 15)
            pygame.draw.line(
                self.screen, (cor_r, cor_g, cor_b), (0, y), (self.largura, y)
            )

    def desenhar_particulas(self):
        """Desenha partículas animadas no fundo"""
        for i in range(20):
            x = (i * 137 + self.tempo_animacao) % self.largura
            y = (i * 73 + self.tempo_animacao // 2) % self.altura
            alpha = 50 + 30 * (i % 3)
            if alpha > 255:
                alpha = 255
            pygame.draw.circle(
                self.screen, (255, 255, 255, min(alpha, 255)), (int(x), int(y)), 1
            )

    def desenhar_botao(self, botao, index, mouse_pos):
        """Desenha um botão com efeitos visuais"""
        hover = (
            botao["rect"].collidepoint(mouse_pos) or index == self.botao_selecionado
        )

        # Cor do botão
        cor = self.cor_botao_hover if hover else self.cor_botao

        # Sombra
        sombra_rect = botao["rect"].copy()
        sombra_rect.x += 3
        sombra_rect.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 100), sombra_rect, border_radius=10)

        # Botão principal
        pygame.draw.rect(self.screen, cor, botao["rect"], border_radius=10)

        # Borda se selecionado
        if hover:
            pygame.draw.rect(
                self.screen, self.cor_primaria, botao["rect"], 2, border_radius=10
            )

        # Texto
        texto_surface = self.fonte_botao.render(
            botao["texto"], True, self.cor_texto
        )
        texto_rect = texto_surface.get_rect(center=botao["rect"].center)
        self.screen.blit(texto_surface, texto_rect)

    def desenhar_menu_principal(self, mouse_pos):
        """Desenha o menu principal"""
        titulo = self.fonte_titulo.render("REAPERQUEST", True, self.cor_primaria)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 150))
        self.screen.blit(titulo, titulo_rect)

        # Desenha o seletor de dificuldade
        dificuldade_texto = self.fonte_subtitulo.render(
            f"Dificuldade: {self.dificuldade_atual}",
            True,
            self.cores_dificuldade[self.dificuldade_atual]
        )
        dificuldade_rect = dificuldade_texto.get_rect()
        dificuldade_rect.topright = (self.largura - 20, 20)
        self.screen.blit(dificuldade_texto, dificuldade_rect)

        # Desenha instruções de dificuldade
        instrucoes = self.fonte_subtitulo.render(
            "← → para mudar dificuldade",
            True,
            self.cor_texto_secundario
        )
        instrucoes_rect = instrucoes.get_rect()
        instrucoes_rect.topright = (self.largura - 20, 60)
        self.screen.blit(instrucoes, instrucoes_rect)

        # Desenha botões
        for i, botao in enumerate(self.botoes):
            self.desenhar_botao(botao, i, mouse_pos)

    def desenhar_ranking(self, mouse_pos):
        """Desenha a tela de ranking"""
        titulo = self.fonte_titulo.render("RANKING", True, self.cor_primaria)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 80))
        self.screen.blit(titulo, titulo_rect)

        # Cabeçalhos das colunas
        cabecalho_y = 130
        pos_header = self.fonte_texto.render("#", True, self.cor_acento)
        self.screen.blit(pos_header, (100, cabecalho_y))
        
        nome_header = self.fonte_texto.render("NOME", True, self.cor_acento)
        self.screen.blit(nome_header, (140, cabecalho_y))
        
        tempo_header = self.fonte_texto.render("TEMPO", True, self.cor_acento)
        self.screen.blit(tempo_header, (320, cabecalho_y))
        
        data_header = self.fonte_texto.render("DATA", True, self.cor_acento)
        self.screen.blit(data_header, (420, cabecalho_y))
        
        hora_header = self.fonte_texto.render("HORA", True, self.cor_acento)
        self.screen.blit(hora_header, (520, cabecalho_y))

        # Lista os records
        y_start = 160
        for i, record in enumerate(self.ranking_data[:10]):
            y_pos = y_start + i * 30

            # Posição
            pos_text = self.fonte_texto.render(f"{i+1}.", True, self.cor_acento)
            self.screen.blit(pos_text, (100, y_pos))

            # Nome (limitado a 12 caracteres)
            nome_display = record["nome"][:12] + "..." if len(record["nome"]) > 12 else record["nome"]
            nome_text = self.fonte_texto.render(
                nome_display, True, self.cor_texto
            )
            self.screen.blit(nome_text, (140, y_pos))

            # Tempo
            if "tempo" in record:
                tempo_segundos = record["tempo"]
                minutos = tempo_segundos // 60
                segundos = tempo_segundos % 60
                tempo_text = self.fonte_texto.render(
                    f"{minutos:02d}:{segundos:02d}", True, self.cor_texto_secundario
                )
            elif "distancia" in record:
                tempo_text = self.fonte_texto.render(
                    f"{record['distancia']}", True, self.cor_texto_secundario
                )
            else:
                tempo_text = self.fonte_texto.render(
                    "--:--", True, self.cor_texto_secundario
                )
            self.screen.blit(tempo_text, (320, y_pos))

            # Data
            if "data" in record:
                data_text = self.fonte_texto.render(
                    record["data"], True, self.cor_texto_secundario
                )
            else:
                data_text = self.fonte_texto.render(
                    "--/--/--", True, self.cor_texto_secundario
                )
            self.screen.blit(data_text, (420, y_pos))
            
            # Hora
            if "hora" in record:
                hora_text = self.fonte_texto.render(
                    record["hora"], True, self.cor_texto_secundario
                )
            else:
                hora_text = self.fonte_texto.render(
                    "--:--:--", True, self.cor_texto_secundario
                )
            self.screen.blit(hora_text, (520, y_pos))

        if not self.ranking_data:
            texto = self.fonte_subtitulo.render(
                "Nenhum record ainda!", True, self.cor_texto_secundario
            )
            texto_rect = texto.get_rect(center=(self.largura // 2, 300))
            self.screen.blit(texto, texto_rect)

        # Desenha botões
        for i, botao in enumerate(self.botoes):
            self.desenhar_botao(botao, i, mouse_pos)

    def desenhar_input_nome(self, mouse_pos):
        """Desenha a tela de input de nome"""
        titulo = self.fonte_titulo.render(
            "DIGITE SEU NOME", True, self.cor_primaria
        )
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

        # Texto do input com cursor piscando
        texto_input = self.nome_jogador + (
            "_" if self.input_ativo and (self.tempo_animacao // 30) % 2 else ""
        )

        # Cor do texto baseada no estado
        if not self.nome_jogador.strip():
            cor_texto = self.cor_texto_secundario
        else:
            cor_texto = self.cor_texto

        texto_surface = self.fonte_botao.render(texto_input, True, cor_texto)
        texto_rect = texto_surface.get_rect(center=input_rect.center)
        self.screen.blit(texto_surface, texto_rect)

        # Desenha botões
        for i, botao in enumerate(self.botoes):
            self.desenhar_botao(botao, i, mouse_pos)

    def desenhar_game_over(self, mouse_pos):
        """Desenha a tela de game over"""
        titulo = self.fonte_titulo.render("GAME OVER", True, self.cor_acento)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 200))
        self.screen.blit(titulo, titulo_rect)

        # Mensagem personalizada
        if self.nome_jogador:
            msg = self.fonte_subtitulo.render(
                f"Boa tentativa, {self.nome_jogador}!", True, self.cor_texto
            )
            msg_rect = msg.get_rect(center=(self.largura // 2, 260))
            self.screen.blit(msg, msg_rect)

        # Desenha botões
        for i, botao in enumerate(self.botoes):
            self.desenhar_botao(botao, i, mouse_pos)

    def desenhar_vitoria(self, mouse_pos):
        """Desenha a tela de vitória"""
        titulo = self.fonte_titulo.render("VITÓRIA!", True, self.cor_primaria)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 150))
        self.screen.blit(titulo, titulo_rect)

        # Mensagem personalizada
        if self.nome_jogador:
            msg = self.fonte_subtitulo.render(
                f"Parabéns, {self.nome_jogador}!", True, self.cor_texto
            )
            msg_rect = msg.get_rect(center=(self.largura // 2, 200))
            self.screen.blit(msg, msg_rect)

        # Desenha estatísticas
        y_pos = 250
        estatisticas_texto = [
            "Tempo de jogo: %d:%02d" % (self.tempo_jogo // 60, self.tempo_jogo % 60),
            f"Inimigos derrotados: {self.inimigos_mortos}/{self.total_inimigos}",
            f"Vida restante: {self.vida_restante}/{self.vida_maxima}"
        ]

        for texto in estatisticas_texto:
            stat = self.fonte_texto.render(texto, True, self.cor_texto_secundario)
            stat_rect = stat.get_rect(center=(self.largura // 2, y_pos))
            self.screen.blit(stat, stat_rect)
            y_pos += 30

        # Desenha botões
        for i, botao in enumerate(self.botoes):
            self.desenhar_botao(botao, i, mouse_pos)

    def processar_input_teclado(self, event):
        """Processa input do teclado"""
        if event.type == pygame.KEYDOWN:
            if self.estado == "input_nome" and self.input_ativo:
                if event.key == pygame.K_RETURN:
                    if self.nome_jogador.strip():
                        return {
                            "nome": self.nome_jogador.strip(),
                            "dificuldade": self.dificuldade_atual,
                            "num_inimigos": self.inimigos_por_dificuldade[self.dificuldade_atual]
                        }
                elif event.key == pygame.K_BACKSPACE:
                    self.nome_jogador = self.nome_jogador[:-1]
                elif event.unicode.isprintable() and len(self.nome_jogador) < 20:
                    self.nome_jogador += event.unicode
            else:
                if self.estado == "menu_principal":
                    if event.key == pygame.K_LEFT:
                        atual_index = self.dificuldades.index(self.dificuldade_atual)
                        self.dificuldade_atual = self.dificuldades[(atual_index - 1) % len(self.dificuldades)]
                    elif event.key == pygame.K_RIGHT:
                        atual_index = self.dificuldades.index(self.dificuldade_atual)
                        self.dificuldade_atual = self.dificuldades[(atual_index + 1) % len(self.dificuldades)]
                if event.key == pygame.K_UP:
                    self.botao_selecionado = (self.botao_selecionado - 1) % len(self.botoes)
                elif event.key == pygame.K_DOWN:
                    self.botao_selecionado = (self.botao_selecionado + 1) % len(self.botoes)
                elif event.key == pygame.K_RETURN:
                    if self.botoes:
                        botao = self.botoes[self.botao_selecionado]
                        if botao["acao"]:
                            resultado = botao["acao"]()
                            if botao["texto"] == "CONTINUAR PARTIDA":
                                return "continuar"
                            if resultado and self.estado == "input_nome" and self.nome_jogador.strip() and botao["texto"] == "CONFIRMAR":
                                return {
                                    "nome": self.nome_jogador.strip(),
                                    "dificuldade": self.dificuldade_atual,
                                    "num_inimigos": self.inimigos_por_dificuldade[self.dificuldade_atual]
                                }
        return None

    def processar_input_mouse(self, event, mouse_pos):
        """Processa input do mouse"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.estado == "input_nome":
                input_rect = pygame.Rect(self.largura // 2 - 150, 300, 300, 50)
                self.input_ativo = input_rect.collidepoint(mouse_pos)
            for i, botao in enumerate(self.botoes):
                if botao["rect"].collidepoint(mouse_pos):
                    self.botao_selecionado = i
                    if botao["acao"]:
                        resultado = botao["acao"]()
                        if botao["texto"] == "CONTINUAR PARTIDA":
                            return "continuar"
                        if resultado and self.estado == "input_nome" and self.nome_jogador.strip() and botao["texto"] == "CONFIRMAR":
                            return {
                                "nome": self.nome_jogador.strip(),
                                "dificuldade": self.dificuldade_atual,
                                "num_inimigos": self.inimigos_por_dificuldade[self.dificuldade_atual]
                            }
        elif event.type == pygame.MOUSEMOTION:
            for i, botao in enumerate(self.botoes):
                if botao["rect"].collidepoint(mouse_pos):
                    self.botao_selecionado = i
                    break
        return None

    def run(self):
        """Loop principal do menu"""
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            self.tempo_animacao += 1

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
            elif self.estado == "vitoria":
                self.desenhar_vitoria(mouse_pos)

            pygame.display.flip()
            self.clock.tick(60)

        print(f"Menu finalizado - Nome: {self.nome_jogador}")
        if self.nome_jogador and self.nome_jogador.strip():
            return {
                "nome": self.nome_jogador.strip(),
                "dificuldade": self.dificuldade_atual,
                "num_inimigos": self.inimigos_por_dificuldade[self.dificuldade_atual]
            }
        return None
