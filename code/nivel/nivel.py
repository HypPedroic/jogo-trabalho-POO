# Importando as bibliotecas necessárias
import pygame
import random
from entidades.inimigo_terrestre import InimigoTerrestre
from entidades.inimigo_suicida import InimigoSuicida

# Classe para gerenciar o nível do jogo
class Nivel:
    def __init__(self, game):
        self.__game = game
        self.__largura_nivel = 10000  # Largura total do nível em pixels
        self.__dificuldade = 1  # Nível de dificuldade (aumenta com a distância)
        self.__distancia_ultimo_inimigo = 0  # Distância desde o último inimigo gerado
        self.__distancia_minima_inimigos = 300  # Distância mínima entre inimigos
        self.__chance_inimigo_terrestre = 70  # Porcentagem de chance de gerar inimigo terrestre
        self.__chance_inimigo_suicida = 30  # Porcentagem de chance de gerar inimigo suicida
        self.__inimigos_gerados = False  # Flag para controlar a geração de inimigos
        
        # Posições dos tiles de plataforma
        self.__plataformas = []
        
        # Gera o nível inicial
        self.__gerar_nivel()
    
    @property
    def game(self):
        return self.__game
    
    @property
    def dificuldade(self):
        return self.__dificuldade
    
    def __gerar_nivel(self):
        """Gera o nível inicial com plataformas e obstáculos"""
        # Limpa o tilemap atual
        self.__game.tilemap.tilemap = {}
        
        # Gera o chão base
        for x in range(self.__largura_nivel // self.__game.tilemap.tile_size):
            self.__game.tilemap.tilemap[f"{x};14"] = {
                'type': 'grass',
                'variant': random.randint(0, 5),
                'pos': (x, 14)
            }
        
        # Gera plataformas flutuantes
        plataformas_geradas = 0
        x = 10  # Começa após uma certa distância do início
        
        while x < (self.__largura_nivel // self.__game.tilemap.tile_size) - 10:
            # Decide se vai gerar uma plataforma
            if random.random() < 0.3:  # 30% de chance
                # Determina o comprimento da plataforma
                comprimento = random.randint(3, 8)
                
                # Determina a altura da plataforma
                altura = random.randint(8, 12)
                
                # Gera a plataforma
                for i in range(comprimento):
                    if x + i < (self.__largura_nivel // self.__game.tilemap.tile_size):
                        self.__game.tilemap.tilemap[f"{x + i};{altura}"] = {
                            'type': 'grass',
                            'variant': random.randint(0, 5),
                            'pos': (x + i, altura)
                        }
                        
                        # Adiciona a posição da plataforma à lista
                        self.__plataformas.append((x + i, altura))
                
                # Avança além da plataforma gerada
                x += comprimento + random.randint(5, 15)
                plataformas_geradas += 1
            else:
                # Avança um pouco
                x += random.randint(5, 10)
        
        # Gera obstáculos estilo Mario
        self.__gerar_obstaculos_mario()
    
    def __gerar_obstaculos_mario(self):
        """Gera obstáculos estilo Mario como blocos, canos e plataformas"""
        # Gera blocos de tijolos e blocos de interrogação
        for _ in range(50):
            x = random.randint(15, (self.__largura_nivel // self.__game.tilemap.tile_size) - 15)
            y = random.randint(10, 13)  # Altura variável para os blocos
            
            # Verifica se não há nada nessa posição
            if f"{x};{y}" not in self.__game.tilemap.tilemap:
                # 50% de chance de ser um bloco de tijolos, 50% de ser um bloco de interrogação
                if random.random() < 0.5:
                    tipo = 'grass'  # Temporariamente usando grass para tijolos
                    variante = 0
                else:
                    tipo = 'grass'  # Temporariamente usando grass para blocos de interrogação
                    variante = 1
                
                self.__game.tilemap.tilemap[f"{x};{y}"] = {
                    'type': tipo,
                    'variant': variante,
                    'pos': (x, y)
                }
        
        # Gera canos
        for _ in range(20):
            x = random.randint(20, (self.__largura_nivel // self.__game.tilemap.tile_size) - 20)
            y = 13  # Base do cano (uma posição acima do chão)
            
            # Verifica se não há nada nessa posição e nas posições adjacentes
            if (f"{x};{y}" not in self.__game.tilemap.tilemap and 
                f"{x+1};{y}" not in self.__game.tilemap.tilemap):
                
                # Altura do cano
                altura_cano = random.randint(1, 3)
                
                # Gera o cano (2 blocos de largura)
                for h in range(altura_cano):
                    self.__game.tilemap.tilemap[f"{x};{y-h}"] = {
                        'type': 'grass',  # Temporariamente usando grass para canos
                        'variant': 2,
                        'pos': (x, y-h)
                    }
                    
                    self.__game.tilemap.tilemap[f"{x+1};{y-h}"] = {
                        'type': 'grass',  # Temporariamente usando grass para canos
                        'variant': 2,
                        'pos': (x+1, y-h)
                    }
                
                # Avança para evitar canos muito próximos
                x += random.randint(10, 20)
        
        # Gera escadas de blocos
        for _ in range(15):
            x = random.randint(25, (self.__largura_nivel // self.__game.tilemap.tile_size) - 25)
            y = 13  # Base da escada (uma posição acima do chão)
            
            # Verifica se há espaço suficiente
            espaco_livre = True
            for i in range(4):  # Verifica 4 blocos à frente
                if f"{x+i};{y}" in self.__game.tilemap.tilemap:
                    espaco_livre = False
                    break
            
            if espaco_livre:
                # Gera uma escada de blocos (altura crescente)
                for i in range(4):
                    for j in range(i+1):
                        self.__game.tilemap.tilemap[f"{x+i};{y-j}"] = {
                            'type': 'grass',
                            'variant': random.randint(0, 5),
                            'pos': (x+i, y-j)
                        }
    
    def __atualizar_dificuldade(self):
        """Atualiza o nível de dificuldade baseado na distância percorrida"""
        # A cada 1000 pixels de distância, aumenta a dificuldade
        nova_dificuldade = 1 + int(self.__game.player.distancia_percorrida / 1000)
        
        if nova_dificuldade > self.__dificuldade:
            self.__dificuldade = nova_dificuldade
            
            # Ajusta os parâmetros de dificuldade
            self.__distancia_minima_inimigos = max(100, 300 - (self.__dificuldade * 20))
    
    def __gerar_inimigos(self):
        """Gera inimigos ao longo do nível"""
        # Gera inimigos a cada distancia_minima_inimigos pixels
        for x in range(500, self.__largura_nivel, self.__distancia_minima_inimigos):
            # Chance de gerar um inimigo baseado na dificuldade
            if random.randint(1, 100) <= min(30 + self.__dificuldade * 5, 80):
                # Determina o tipo de inimigo
                tipo_inimigo = random.randint(1, 100)
                
                # Inimigo terrestre
                if tipo_inimigo <= self.__chance_inimigo_terrestre:
                    inimigo = InimigoTerrestre(self.__game, (x, 0))
                    self.__game.inimigos.append(inimigo)
                # Inimigo suicida
                else:
                    inimigo = InimigoSuicida(self.__game, (x, 0))
                    self.__game.inimigos.append(inimigo)
        if self.__inimigos_gerados:
            return
        
        # Limpa a lista de inimigos atual
        self.__game.inimigos = []
        
        # Gera inimigos ao longo do nível
        x = 500  # Começa após uma certa distância do início
        
        while x < self.__largura_nivel - 500:
            # Decide se vai gerar um inimigo
            if random.random() < 0.7:  # 70% de chance
                # Determina o tipo de inimigo
                tipo_inimigo = random.randint(1, 100)
                
                if tipo_inimigo <= self.__chance_inimigo_terrestre:
                    # Gera um inimigo terrestre no chão
                    pos = (x, 13 * self.__game.tilemap.tile_size - 32)  # Posição acima do chão
                    self.__game.inimigos.append(InimigoTerrestre(self.__game, pos))
                else:
                    # Gera um inimigo suicida
                    pos = (x, 13 * self.__game.tilemap.tile_size - 32)  # Posição acima do chão
                    self.__game.inimigos.append(InimigoSuicida(self.__game, pos))
                
                # Avança além do inimigo gerado
                x += random.randint(int(self.__distancia_minima_inimigos), int(self.__distancia_minima_inimigos * 1.5))
            else:
                # Avança um pouco
                x += random.randint(100, 200)
        
        self.__inimigos_gerados = True
    
    def __verificar_geracao_inimigos(self):
        """Verifica se é necessário gerar novos inimigos conforme o jogador avança"""
        # Calcula a distância percorrida pelo jogador
        distancia_jogador = self.__game.player.distancia_percorrida
        
        # Se o jogador avançou o suficiente desde o último inimigo gerado
        if distancia_jogador - self.__distancia_ultimo_inimigo >= self.__distancia_minima_inimigos:
            # Chance de gerar um inimigo baseado na dificuldade
            if random.randint(1, 100) <= min(30 + self.__dificuldade * 5, 80):
                # Posição x do inimigo (à frente do jogador)
                pos_x = distancia_jogador + 500  # 500 pixels à frente do jogador
                
                # Determina o tipo de inimigo
                tipo_inimigo = random.randint(1, 100)
                
                # Inimigo terrestre
                if tipo_inimigo <= self.__chance_inimigo_terrestre:
                    inimigo = InimigoTerrestre(self.__game, (pos_x, 0))
                    self.__game.inimigos.append(inimigo)
                # Inimigo suicida
                else:
                    inimigo = InimigoSuicida(self.__game, (pos_x, 0))
                    self.__game.inimigos.append(inimigo)
                
                # Atualiza a distância do último inimigo gerado
                self.__distancia_ultimo_inimigo = distancia_jogador
    
    def update(self):
        """Atualiza o estado do nível"""
        # Atualiza a dificuldade
        self.__atualizar_dificuldade()
        
        # Gera inimigos iniciais se ainda não foram gerados
        if not self.__inimigos_gerados:
            self.__gerar_inimigos()
        
        # Verifica se deve gerar novos inimigos
        self.__verificar_geracao_inimigos()
        
        # Remove inimigos que estão muito longe do jogador
        for inimigo in self.__game.inimigos.copy():
            # Se o inimigo está muito longe para trás, remove-o
            if inimigo.pos[0] < self.__game.player.pos[0] - 1000:
                self.__game.inimigos.remove(inimigo)