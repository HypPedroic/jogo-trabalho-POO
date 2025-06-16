# Importando as bibliotecas necessárias
import pygame

# Classe para o HUD (Heads-Up Display)
class HUD:
    def __init__(self, game):
        self.__game = game
        self.__fonte_texto = pygame.font.Font(None, 24)
        self.__fonte_distancia = pygame.font.Font(None, 36)
        self.__cor_texto = (255, 255, 255)
        self.__cor_vida_cheia = (0, 255, 0)  # Verde
        self.__cor_vida_media = (255, 255, 0)  # Amarelo
        self.__cor_vida_baixa = (255, 0, 0)  # Vermelho
        self.__cor_pulo_duplo_disponivel = (0, 191, 255)  # Azul claro
        self.__cor_pulo_duplo_recarregando = (100, 100, 100)  # Cinza
    
    @property
    def game(self):
        return self.__game
    
    def renderizar(self, surf):
        """Renderiza o HUD na tela"""
        self.__renderizar_vida(surf)
        self.__renderizar_distancia(surf)
        self.__renderizar_barra_pulo_duplo(surf)
    
    def __renderizar_vida(self, surf):
        """Renderiza a barra de vida do jogador"""
        # Desenha o texto "Vida:"
        texto_vida = self.__fonte_texto.render("Vida:", True, self.__cor_texto)
        surf.blit(texto_vida, (10, 10))
        
        # Desenha a barra de vida
        vida_maxima = self.__game.player.vida_maxima
        vida_atual = self.__game.player.vida
        
        # Calcula a largura da barra de vida
        largura_maxima = 100
        largura_atual = (vida_atual / vida_maxima) * largura_maxima
        
        # Determina a cor da barra de vida
        if vida_atual > vida_maxima * 0.7:
            cor = self.__cor_vida_cheia
        elif vida_atual > vida_maxima * 0.3:
            cor = self.__cor_vida_media
        else:
            cor = self.__cor_vida_baixa
        
        # Desenha o fundo da barra de vida
        pygame.draw.rect(surf, (50, 50, 50), (60, 10, largura_maxima, 20))
        
        # Desenha a barra de vida atual
        pygame.draw.rect(surf, cor, (60, 10, largura_atual, 20))
        
        # Desenha o contorno da barra de vida
        pygame.draw.rect(surf, self.__cor_texto, (60, 10, largura_maxima, 20), 1)
    
    def __renderizar_distancia(self, surf):
        """Renderiza a distância percorrida pelo jogador"""
        # Calcula a distância em metros (1 pixel = 0.1 metros)
        distancia_metros = int(self.__game.player.distancia_percorrida * 0.1)
        
        # Desenha o texto da distância
        texto_distancia = self.__fonte_distancia.render(f"Distância: {distancia_metros}m", True, self.__cor_texto)
        surf.blit(texto_distancia, (surf.get_width() - texto_distancia.get_width() - 10, 10))
    
    def __renderizar_barra_pulo_duplo(self, surf):
        """Renderiza a barra de recarga do pulo duplo"""
        # Desenha o texto "Pulo Duplo:"
        texto_pulo_duplo = self.__fonte_texto.render("Pulo Duplo:", True, self.__cor_texto)
        surf.blit(texto_pulo_duplo, (10, 40))
        
        # Calcula a largura da barra de recarga
        largura_maxima = 100
        recarga_atual = self.__game.player.tempo_recarga_pulo_duplo
        recarga_maxima = self.__game.player.recarga_maxima_pulo_duplo
        largura_atual = (recarga_atual / recarga_maxima) * largura_maxima
        
        # Determina a cor da barra de recarga
        if self.__game.player.pulo_duplo_disponivel:
            cor = self.__cor_pulo_duplo_disponivel
        else:
            cor = self.__cor_pulo_duplo_recarregando
        
        # Desenha o fundo da barra de recarga
        pygame.draw.rect(surf, (50, 50, 50), (100, 40, largura_maxima, 20))
        
        # Desenha a barra de recarga atual
        pygame.draw.rect(surf, cor, (100, 40, largura_atual, 20))
        
        # Desenha o contorno da barra de recarga
        pygame.draw.rect(surf, self.__cor_texto, (100, 40, largura_maxima, 20), 1)
        
        # Adiciona um ícone ou texto indicando se o pulo duplo está disponível
        if self.__game.player.pulo_duplo_disponivel:
            texto_status = self.__fonte_texto.render("Pronto!", True, self.__cor_texto)
        else:
            texto_status = self.__fonte_texto.render("Recarregando...", True, self.__cor_texto)
        
        surf.blit(texto_status, (210, 40))