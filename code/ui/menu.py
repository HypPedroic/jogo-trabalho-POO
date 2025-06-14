# Importando as bibliotecas necessárias
import pygame
import os
import json

# Classe para o menu do jogo
class Menu:
    def __init__(self, game):
        self.__game = game
        self.__estado = 'menu_principal'  # 'menu_principal', 'game_over', 'ranking'
        self.__opcao_selecionada = 0
        self.__opcoes_menu_principal = ['Iniciar Jogo', 'Ranking', 'Sair']
        self.__opcoes_game_over = ['Jogar Novamente', 'Menu Principal', 'Sair']
        self.__ranking = []
        self.__nome_jogador = 'Jogador'
        self.__carregando_nome = False
        self.__fonte_titulo = pygame.font.Font(None, 72)
        self.__fonte_opcoes = pygame.font.Font(None, 48)
        self.__fonte_texto = pygame.font.Font(None, 36)
        self.__cor_titulo = (255, 255, 0)
        self.__cor_opcao = (255, 255, 255)
        self.__cor_opcao_selecionada = (255, 0, 0)
        self.__cor_texto = (200, 200, 200)
        self.__carregar_ranking()
    
    @property
    def game(self):
        return self.__game
    
    @game.setter
    def game(self, value):
        self.__game = value
    
    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, valor):
        self.__estado = valor
    
    @property
    def opcao_selecionada(self):
        return self.__opcao_selecionada
    
    @opcao_selecionada.setter
    def opcao_selecionada(self, valor):
        self.__opcao_selecionada = valor
    
    def __carregar_ranking(self):
        """Carrega o ranking de jogadores do arquivo"""
        ranking_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'ranking.json')
        try:
            if os.path.exists(ranking_path):
                with open(ranking_path, 'r') as f:
                    self.__ranking = json.load(f)
            else:
                self.__ranking = []
        except Exception as e:
            print(f"Erro ao carregar ranking: {e}")
            self.__ranking = []
    
    def __salvar_ranking(self):
        """Salva o ranking de jogadores no arquivo"""
        ranking_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'ranking.json')
        try:
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(ranking_path), exist_ok=True)
            
            with open(ranking_path, 'w') as f:
                json.dump(self.__ranking, f)
        except Exception as e:
            print(f"Erro ao salvar ranking: {e}")
    
    def adicionar_pontuacao(self, distancia):
        """Adiciona uma nova pontuação ao ranking"""
        # Arredonda a distância para o inteiro mais próximo
        distancia_int = int(distancia)
        
        # Verifica se já existe uma pontuação com o mesmo nome e distância
        pontuacao_existente = False
        for pontuacao in self.__ranking:
            if pontuacao['nome'] == self.__nome_jogador and pontuacao['distancia'] == distancia_int:
                pontuacao_existente = True
                break
        
        # Só adiciona se não existir uma pontuação idêntica
        if not pontuacao_existente:
            self.__ranking.append({'nome': self.__nome_jogador, 'distancia': distancia_int})
            
            # Ordena o ranking pela distância (maior para menor)
            self.__ranking = sorted(self.__ranking, key=lambda x: x['distancia'], reverse=True)
            
            # Limita o ranking às 10 melhores pontuações
            if len(self.__ranking) > 10:
                self.__ranking = self.__ranking[:10]
            
            # Salva o ranking atualizado
            self.__salvar_ranking()
    
    def processar_eventos(self, eventos):
        """Processa os eventos do menu"""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if self.__carregando_nome:
                    # Processamento de entrada de texto para o nome do jogador
                    if evento.key == pygame.K_RETURN:
                        self.__carregando_nome = False
                    elif evento.key == pygame.K_BACKSPACE:
                        self.__nome_jogador = self.__nome_jogador[:-1]
                    elif len(self.__nome_jogador) < 10:  # Limita o tamanho do nome
                        if evento.unicode.isalnum() or evento.unicode == ' ':
                            self.__nome_jogador += evento.unicode
                else:
                    # Navegação no menu
                    if evento.key == pygame.K_UP:
                        self.__opcao_selecionada = (self.__opcao_selecionada - 1) % len(self.__opcoes_menu_principal if self.__estado == 'menu_principal' else self.__opcoes_game_over)
                    elif evento.key == pygame.K_DOWN:
                        self.__opcao_selecionada = (self.__opcao_selecionada + 1) % len(self.__opcoes_menu_principal if self.__estado == 'menu_principal' else self.__opcoes_game_over)
                    elif evento.key == pygame.K_RETURN:
                        self.__selecionar_opcao()
                    elif evento.key == pygame.K_ESCAPE:
                        if self.__estado == 'ranking':
                            self.__estado = 'menu_principal'
                            self.__opcao_selecionada = 0
    
    def __selecionar_opcao(self):
        """Seleciona a opção atual do menu"""
        if self.__estado == 'menu_principal':
            if self.__opcao_selecionada == 0:  # Iniciar Jogo
                self.__carregando_nome = True
                self.__game.iniciar_jogo()
            elif self.__opcao_selecionada == 1:  # Ranking
                self.__estado = 'ranking'
            elif self.__opcao_selecionada == 2:  # Sair
                self.__game.running = False
        
        elif self.__estado == 'game_over':
            if self.__opcao_selecionada == 0:  # Jogar Novamente
                self.__game.iniciar_jogo()
            elif self.__opcao_selecionada == 1:  # Menu Principal
                self.__estado = 'menu_principal'
                self.__opcao_selecionada = 0
            elif self.__opcao_selecionada == 2:  # Sair
                self.__game.running = False
    
    def renderizar(self, surf):
        """Renderiza o menu na tela"""
        # Limpa a tela
        surf.fill((0, 0, 0))
        
        if self.__estado == 'menu_principal':
            self.__renderizar_menu_principal(surf)
        elif self.__estado == 'game_over':
            self.__renderizar_game_over(surf)
        elif self.__estado == 'ranking':
            self.__renderizar_ranking(surf)
        
        if self.__carregando_nome:
            self.__renderizar_entrada_nome(surf)
    
    def __renderizar_menu_principal(self, surf):
        """Renderiza o menu principal"""
        # Renderiza o título
        titulo = self.__fonte_titulo.render("RUN OR DIE", True, self.__cor_titulo)
        surf.blit(titulo, (surf.get_width() // 2 - titulo.get_width() // 2, 100))
        
        # Renderiza as opções do menu
        for i, opcao in enumerate(self.__opcoes_menu_principal):
            cor = self.__cor_opcao_selecionada if i == self.__opcao_selecionada else self.__cor_opcao
            texto = self.__fonte_opcoes.render(opcao, True, cor)
            surf.blit(texto, (surf.get_width() // 2 - texto.get_width() // 2, 250 + i * 60))
        
        # Renderiza o ranking no canto da tela
        self.__renderizar_mini_ranking(surf)
    
    def __renderizar_game_over(self, surf):
        """Renderiza a tela de game over"""
        # Renderiza o título
        titulo = self.__fonte_titulo.render("Game Over", True, self.__cor_titulo)
        surf.blit(titulo, (surf.get_width() // 2 - titulo.get_width() // 2, 100))
        
        # Renderiza a pontuação
        pontuacao = self.__fonte_texto.render(f"Distância percorrida: {int(self.__game.player.get_distancia_percorrida())}", True, self.__cor_texto)
        surf.blit(pontuacao, (surf.get_width() // 2 - pontuacao.get_width() // 2, 180))
        
        # Renderiza as opções do menu
        for i, opcao in enumerate(self.__opcoes_game_over):
            cor = self.__cor_opcao_selecionada if i == self.__opcao_selecionada else self.__cor_opcao
            texto = self.__fonte_opcoes.render(opcao, True, cor)
            surf.blit(texto, (surf.get_width() // 2 - texto.get_width() // 2, 250 + i * 60))
    
    def __renderizar_ranking(self, surf):
        """Renderiza a tela de ranking"""
        # Renderiza o título
        titulo = self.__fonte_titulo.render("Ranking", True, self.__cor_titulo)
        surf.blit(titulo, (surf.get_width() // 2 - titulo.get_width() // 2, 50))
        
        # Renderiza as pontuações
        if len(self.__ranking) > 0:
            for i, pontuacao in enumerate(self.__ranking):
                texto = self.__fonte_texto.render(f"{i+1}. {pontuacao['nome']}: {pontuacao['distancia']}", True, self.__cor_texto)
                surf.blit(texto, (surf.get_width() // 2 - texto.get_width() // 2, 150 + i * 40))
        else:
            texto = self.__fonte_texto.render("Nenhuma pontuação registrada", True, self.__cor_texto)
            surf.blit(texto, (surf.get_width() // 2 - texto.get_width() // 2, 200))
        
        # Renderiza a instrução para voltar
        voltar = self.__fonte_texto.render("Pressione ESC para voltar", True, self.__cor_texto)
        surf.blit(voltar, (surf.get_width() // 2 - voltar.get_width() // 2, surf.get_height() - 50))
    
    def __renderizar_mini_ranking(self, surf):
        """Renderiza um mini ranking no canto da tela"""
        # Renderiza o título do mini ranking
        titulo = self.__fonte_texto.render("Top 5", True, self.__cor_texto)
        surf.blit(titulo, (surf.get_width() - 200, 50))
        
        # Renderiza as pontuações
        for i, pontuacao in enumerate(self.__ranking[:5]):  # Mostra apenas os 5 primeiros
            texto = self.__fonte_texto.render(f"{i+1}. {pontuacao['nome']}: {pontuacao['distancia']}", True, self.__cor_texto)
            surf.blit(texto, (surf.get_width() - 200, 90 + i * 30))
    
    def __renderizar_entrada_nome(self, surf):
        """Renderiza a caixa de entrada de nome"""
        # Cria um retângulo semi-transparente para o fundo
        s = pygame.Surface((400, 200))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        surf.blit(s, (surf.get_width() // 2 - 200, surf.get_height() // 2 - 100))
        
        # Renderiza o título
        titulo = self.__fonte_texto.render("Digite seu nome:", True, self.__cor_texto)
        surf.blit(titulo, (surf.get_width() // 2 - titulo.get_width() // 2, surf.get_height() // 2 - 50))
        
        # Renderiza o nome
        nome = self.__fonte_texto.render(self.__nome_jogador + "_", True, self.__cor_texto)
        surf.blit(nome, (surf.get_width() // 2 - nome.get_width() // 2, surf.get_height() // 2))
        
        # Renderiza a instrução
        instrucao = self.__fonte_texto.render("Pressione ENTER para confirmar", True, self.__cor_texto)
        surf.blit(instrucao, (surf.get_width() // 2 - instrucao.get_width() // 2, surf.get_height() // 2 + 50))