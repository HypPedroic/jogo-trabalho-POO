# Importando as bibliotecas necessárias
import pygame
import os
import json

# Classe para o menu do jogo
class Menu:
    def __init__(self, game):
        self.game = game
        self.estado = 'menu_principal'  # 'menu_principal', 'game_over', 'ranking'
        self.opcao_selecionada = 0
        self.opcoes_menu_principal = ['Iniciar Jogo', 'Ranking', 'Sair']
        self.opcoes_game_over = ['Jogar Novamente', 'Menu Principal', 'Sair']
        self.ranking = []
        self.nome_jogador = 'Jogador'
        self.carregando_nome = False
        self.fonte_titulo = pygame.font.Font(None, 72)
        self.fonte_opcoes = pygame.font.Font(None, 48)
        self.fonte_texto = pygame.font.Font(None, 36)
        self.cor_titulo = (255, 255, 0)
        self.cor_opcao = (255, 255, 255)
        self.cor_opcao_selecionada = (255, 0, 0)
        self.cor_texto = (200, 200, 200)
        self.carregar_ranking()
    
    def carregar_ranking(self):
        """Carrega o ranking de jogadores do arquivo"""
        ranking_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'ranking.json')
        try:
            if os.path.exists(ranking_path):
                with open(ranking_path, 'r') as f:
                    self.ranking = json.load(f)
            else:
                self.ranking = []
        except Exception as e:
            print(f"Erro ao carregar ranking: {e}")
            self.ranking = []
    
    def salvar_ranking(self):
        """Salva o ranking de jogadores no arquivo"""
        ranking_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'ranking.json')
        try:
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(ranking_path), exist_ok=True)
            
            with open(ranking_path, 'w') as f:
                json.dump(self.ranking, f)
        except Exception as e:
            print(f"Erro ao salvar ranking: {e}")
    
    def adicionar_pontuacao(self, distancia):
        """Adiciona uma nova pontuação ao ranking"""
        # Arredonda a distância para o inteiro mais próximo
        distancia_int = int(distancia)
        
        # Adiciona a nova pontuação
        self.ranking.append({'nome': self.nome_jogador, 'distancia': distancia_int})
        
        # Ordena o ranking pela distância (maior para menor)
        self.ranking = sorted(self.ranking, key=lambda x: x['distancia'], reverse=True)
        
        # Limita o ranking às 10 melhores pontuações
        if len(self.ranking) > 10:
            self.ranking = self.ranking[:10]
        
        # Salva o ranking atualizado
        self.salvar_ranking()
    
    def processar_eventos(self, eventos):
        """Processa os eventos do menu"""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if self.carregando_nome:
                    # Processamento de entrada de texto para o nome do jogador
                    if evento.key == pygame.K_RETURN:
                        self.carregando_nome = False
                    elif evento.key == pygame.K_BACKSPACE:
                        self.nome_jogador = self.nome_jogador[:-1]
                    elif len(self.nome_jogador) < 10:  # Limita o tamanho do nome
                        if evento.unicode.isalnum() or evento.unicode == ' ':
                            self.nome_jogador += evento.unicode
                else:
                    # Navegação no menu
                    if evento.key == pygame.K_UP:
                        self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes_menu_principal if self.estado == 'menu_principal' else self.opcoes_game_over)
                    elif evento.key == pygame.K_DOWN:
                        self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes_menu_principal if self.estado == 'menu_principal' else self.opcoes_game_over)
                    elif evento.key == pygame.K_RETURN:
                        self.selecionar_opcao()
                    elif evento.key == pygame.K_ESCAPE:
                        if self.estado == 'ranking':
                            self.estado = 'menu_principal'
                            self.opcao_selecionada = 0
    
    def selecionar_opcao(self):
        """Seleciona a opção atual do menu"""
        if self.estado == 'menu_principal':
            if self.opcao_selecionada == 0:  # Iniciar Jogo
                self.carregando_nome = True
                self.game.iniciar_jogo()
            elif self.opcao_selecionada == 1:  # Ranking
                self.estado = 'ranking'
            elif self.opcao_selecionada == 2:  # Sair
                self.game.running = False
        
        elif self.estado == 'game_over':
            if self.opcao_selecionada == 0:  # Jogar Novamente
                self.game.iniciar_jogo()
            elif self.opcao_selecionada == 1:  # Menu Principal
                self.estado = 'menu_principal'
                self.opcao_selecionada = 0
            elif self.opcao_selecionada == 2:  # Sair
                self.game.running = False
    
    def renderizar(self, surf):
        """Renderiza o menu na tela"""
        # Limpa a tela
        surf.fill((0, 0, 0))
        
        if self.estado == 'menu_principal':
            self.renderizar_menu_principal(surf)
        elif self.estado == 'game_over':
            self.renderizar_game_over(surf)
        elif self.estado == 'ranking':
            self.renderizar_ranking(surf)
        
        if self.carregando_nome:
            self.renderizar_entrada_nome(surf)
    
    def renderizar_menu_principal(self, surf):
        """Renderiza o menu principal"""
        # Renderiza o título
        titulo = self.fonte_titulo.render("Super Mario Clone", True, self.cor_titulo)
        surf.blit(titulo, (surf.get_width() // 2 - titulo.get_width() // 2, 100))
        
        # Renderiza as opções do menu
        for i, opcao in enumerate(self.opcoes_menu_principal):
            cor = self.cor_opcao_selecionada if i == self.opcao_selecionada else self.cor_opcao
            texto = self.fonte_opcoes.render(opcao, True, cor)
            surf.blit(texto, (surf.get_width() // 2 - texto.get_width() // 2, 250 + i * 60))
        
        # Renderiza o ranking no canto da tela
        self.renderizar_mini_ranking(surf)
    
    def renderizar_game_over(self, surf):
        """Renderiza a tela de game over"""
        # Renderiza o título
        titulo = self.fonte_titulo.render("Game Over", True, self.cor_titulo)
        surf.blit(titulo, (surf.get_width() // 2 - titulo.get_width() // 2, 100))
        
        # Renderiza a pontuação
        pontuacao = self.fonte_texto.render(f"Distância percorrida: {int(self.game.player.distancia_percorrida)}", True, self.cor_texto)
        surf.blit(pontuacao, (surf.get_width() // 2 - pontuacao.get_width() // 2, 180))
        
        # Renderiza as opções do menu
        for i, opcao in enumerate(self.opcoes_game_over):
            cor = self.cor_opcao_selecionada if i == self.opcao_selecionada else self.cor_opcao
            texto = self.fonte_opcoes.render(opcao, True, cor)
            surf.blit(texto, (surf.get_width() // 2 - texto.get_width() // 2, 250 + i * 60))
    
    def renderizar_ranking(self, surf):
        """Renderiza a tela de ranking"""
        # Renderiza o título
        titulo = self.fonte_titulo.render("Ranking", True, self.cor_titulo)
        surf.blit(titulo, (surf.get_width() // 2 - titulo.get_width() // 2, 50))
        
        # Renderiza as pontuações
        if len(self.ranking) > 0:
            for i, pontuacao in enumerate(self.ranking):
                texto = self.fonte_texto.render(f"{i+1}. {pontuacao['nome']}: {pontuacao['distancia']}", True, self.cor_texto)
                surf.blit(texto, (surf.get_width() // 2 - texto.get_width() // 2, 150 + i * 40))
        else:
            texto = self.fonte_texto.render("Nenhuma pontuação registrada", True, self.cor_texto)
            surf.blit(texto, (surf.get_width() // 2 - texto.get_width() // 2, 200))
        
        # Renderiza a instrução para voltar
        voltar = self.fonte_texto.render("Pressione ESC para voltar", True, self.cor_texto)
        surf.blit(voltar, (surf.get_width() // 2 - voltar.get_width() // 2, surf.get_height() - 50))
    
    def renderizar_mini_ranking(self, surf):
        """Renderiza um mini ranking no canto da tela"""
        # Renderiza o título do mini ranking
        titulo = self.fonte_texto.render("Top 5", True, self.cor_texto)
        surf.blit(titulo, (surf.get_width() - 200, 50))
        
        # Renderiza as pontuações
        for i, pontuacao in enumerate(self.ranking[:5]):  # Mostra apenas os 5 primeiros
            texto = self.fonte_texto.render(f"{i+1}. {pontuacao['nome']}: {pontuacao['distancia']}", True, self.cor_texto)
            surf.blit(texto, (surf.get_width() - 200, 90 + i * 30))
    
    def renderizar_entrada_nome(self, surf):
        """Renderiza a caixa de entrada de nome"""
        # Cria um retângulo semi-transparente para o fundo
        s = pygame.Surface((400, 200))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        surf.blit(s, (surf.get_width() // 2 - 200, surf.get_height() // 2 - 100))
        
        # Renderiza o título
        titulo = self.fonte_texto.render("Digite seu nome:", True, self.cor_texto)
        surf.blit(titulo, (surf.get_width() // 2 - titulo.get_width() // 2, surf.get_height() // 2 - 50))
        
        # Renderiza o nome
        nome = self.fonte_texto.render(self.nome_jogador + "_", True, self.cor_texto)
        surf.blit(nome, (surf.get_width() // 2 - nome.get_width() // 2, surf.get_height() // 2))
        
        # Renderiza a instrução
        instrucao = self.fonte_texto.render("Pressione ENTER para confirmar", True, self.cor_texto)
        surf.blit(instrucao, (surf.get_width() // 2 - instrucao.get_width() // 2, surf.get_height() // 2 + 50))