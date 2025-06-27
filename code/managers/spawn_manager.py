# Importando as bibliotecas necessárias
import pygame
import random
from entidades.slime import Slime
from entidades.esqueleto import Esqueleto

class SpawnManager:
    def __init__(self, tilemap, player, num_inimigos=15, game=None):
        self.__tilemap = tilemap
        self.__player = player
        self.__inimigos_ativos = []
        self.__inimigos_pool = []
        self.__max_inimigos = num_inimigos  # Quantidade de inimigos no mapa baseada na dificuldade
        self.__inimigos_totais = num_inimigos  # Total de inimigos que existirão no jogo
        self.__inimigos_mortos = 0  # Contador de inimigos mortos
        self.__posicoes_spawn = []
        self.__ultimo_spawn = 0
        self.__intervalo_spawn = 5000  # 5 segundos
        self.__game = game  # Referência para o jogo (para sons e projéteis)
        
        # Sistema de limbo - inimigos morrem se caírem muito baixo
        self.__limite_limbo_y = 1000  # Distância abaixo do mapa onde inimigos morrem
        
        # Pré-cria pool de inimigos
        self.__inicializar_pool()
        
        # Calcula posições válidas de spawn
        self.__calcular_posicoes_spawn()
    
    @property
    def game(self):
        return self.__game
    
    @game.setter
    def game(self, value):
        self.__game = value
        
    @property
    def tilemap(self):
        return self.__tilemap

    @tilemap.setter
    def tilemap(self, value):
        self.__tilemap = value

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        self.__player = value

    @property
    def inimigos_ativos(self):
        return self.__inimigos_ativos

    @inimigos_ativos.setter
    def inimigos_ativos(self, value):
        self.__inimigos_ativos = value

    @property
    def inimigos_pool(self):
        return self.__inimigos_pool

    @inimigos_pool.setter
    def inimigos_pool(self, value):
        self.__inimigos_pool = value

    @property
    def max_inimigos(self):
        return self.__max_inimigos

    @max_inimigos.setter
    def max_inimigos(self, value):
        self.__max_inimigos = value

    @property
    def inimigos_totais(self):
        return self.__inimigos_totais

    @inimigos_totais.setter
    def inimigos_totais(self, value):
        self.__inimigos_totais = value

    @property
    def inimigos_mortos(self):
        return self.__inimigos_mortos

    @inimigos_mortos.setter
    def inimigos_mortos(self, value):
        self.__inimigos_mortos = value

    @property
    def posicoes_spawn(self):
        return self.__posicoes_spawn

    @posicoes_spawn.setter
    def posicoes_spawn(self, value):
        self.__posicoes_spawn = value

    @property
    def ultimo_spawn(self):
        return self.__ultimo_spawn

    @ultimo_spawn.setter
    def ultimo_spawn(self, value):
        self.__ultimo_spawn = value

    @property
    def intervalo_spawn(self):
        return self.__intervalo_spawn

    @intervalo_spawn.setter
    def intervalo_spawn(self, value):
        self.__intervalo_spawn = value

    @property
    def game(self):
        return self.__game

    @game.setter
    def game(self, value):
        self.__game = value

    @property
    def limite_limbo_y(self):
        return self.__limite_limbo_y

    @limite_limbo_y.setter
    def limite_limbo_y(self, value):
        self.__limite_limbo_y = value
    
    def __calcular_posicoes_spawn(self):
        """Calcula posições válidas para spawn de inimigos"""
        self.posicoes_spawn = []
        tilemap = self.tilemap
        
        # Encontra os limites do mapa baseado nos tiles existentes
        if not tilemap.tilemap:
            return
            
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for loc in tilemap.tilemap:
            # Suporte para diferentes formatos de coordenadas
            if isinstance(loc, str):
                if ';' in loc:
                    x, y = map(int, loc.split(';'))
                elif ',' in loc:
                    coords = loc.strip('()').split(', ')
                    x, y = int(coords[0]), int(coords[1])
                else:
                    continue
            else:
                x, y = loc
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        
        # Percorre o mapa procurando por superfícies sólidas
        for tile_x in range(min_x, max_x + 1):
            for tile_y in range(min_y, max_y + 1):
                # Tenta diferentes formatos de chave
                possible_keys = [
                    f"{tile_x};{tile_y}",
                    f"({tile_x}, {tile_y})",
                    (tile_x, tile_y)
                ]
                
                tile_found = None
                for key in possible_keys:
                    if key in tilemap.tilemap:
                        tile_found = tilemap.tilemap[key]
                        break
                
                if tile_found and tile_found['type'] in tilemap.FISICA_ATIVADA:
                    # Evita spawn no topo do mapa (primeiros 3 tiles de altura)
                    if tile_y <= min_y + 3:
                        continue
                        
                    # Verifica se há espaço livre acima para spawn
                    spawn_keys = [
                        f"{tile_x};{tile_y - 1}",
                        f"({tile_x}, {tile_y - 1})",
                        (tile_x, tile_y - 1)
                    ]
                    
                    spawn_free = True
                    for spawn_key in spawn_keys:
                        if spawn_key in tilemap.tilemap:
                            spawn_free = False
                            break
                    
                    if spawn_free:
                        spawn_x = tile_x * tilemap.tile_size
                        # Ajusta altura para ficar mais acima do chão (16 pixels acima)
                        spawn_y = (tile_y - 1) * tilemap.tile_size - 16
                        self.posicoes_spawn.append((spawn_x, spawn_y))
    
    def __inicializar_pool(self):
        """Inicializa a pool de inimigos"""
        for i in range(self.max_inimigos):
            if random.choice([True, False]):
                slime = Slime((0, 0), (16, 16))
                self.inimigos_pool.append(slime)
            else:
                esqueleto = Esqueleto((0, 0), (32, 32), game=self.game) 
                self.inimigos_pool.append(esqueleto)

    
    def __obter_inimigo_da_pool(self):
        """Obtém um inimigo da pool ou cria um novo se necessário"""
        if self.inimigos_pool:
            return self.inimigos_pool.pop()
        return None
    
    def __retornar_inimigo_para_pool(self, inimigo):
        """Retorna um inimigo para a pool"""
        inimigo.reset()  # Reseta o estado do inimigo
        self.inimigos_pool.append(inimigo)
    
    def __spawn_inimigo(self):
        """Spawna novos inimigos em posições aleatórias válidas"""
        if not self.posicoes_spawn:
            self.__calcular_posicoes_spawn()
        
        if not self.posicoes_spawn:
            print("Nenhuma posição de spawn válida encontrada")
            return
        
        if len(self.inimigos_ativos) >= self.max_inimigos:
            return
        
        # Escolhe uma posição aleatória
        tentativas = 0
        while tentativas < 10:  # Máximo 10 tentativas
            pos_spawn = random.choice(self.posicoes_spawn)
            
            # Verifica distância do jogador (mínimo 100 pixels)
            if self.player:
                distancia_jogador = ((pos_spawn[0] - self.player.pos[0]) ** 2 + 
                                   (pos_spawn[1] - self.player.pos[1]) ** 2) ** 0.5
                if distancia_jogador < 100:
                    tentativas += 1
                    continue
            
            # Verifica distância de outros inimigos (mínimo 150 pixels)
            muito_perto = False
            for inimigo in self.inimigos_ativos:
                distancia_inimigo = ((pos_spawn[0] - inimigo.pos[0]) ** 2 + 
                                   (pos_spawn[1] - inimigo.pos[1]) ** 2) ** 0.5
                if distancia_inimigo < 150:
                    muito_perto = True
                    break
            
            if not muito_perto:
                # Obtém um slime da pool
                novo_slime = self.__obter_inimigo_da_pool()
                if novo_slime:
                    novo_slime.pos = list(pos_spawn)
                    self.inimigos_ativos.append(novo_slime)
                    print(f"Slime spawnado em {pos_spawn}")
                    return
            
            tentativas += 1
        
        print("Não foi possível encontrar posição válida para spawn")
    
    def spawn_todos_inimigos(self):
        """Spawna todos os inimigos do mapa de uma vez"""
        for _ in range(self.inimigos_totais):
            self.__spawn_inimigo()
        print(f"Todos os {self.inimigos_totais} inimigos foram spawnados no mapa!")
    
    def update(self):
        """Atualiza todos os inimigos"""
        for inimigo in self.inimigos_ativos[:]:
            inimigo.update(self.tilemap, self.player)
            
            # Verifica colisão com o player
            if inimigo.estado != 'morto' and self.__verificar_colisao_player(inimigo):
                if inimigo.pode_atacar_jogador_colisao() and self.player.dashing == 0:
                    # Passa referência do game para o ataque
                    if hasattr(self, '_SpawnManager__game'):
                        inimigo.atacar_jogador(self.game)
                    else:
                        inimigo.atacar_jogador()
                elif abs(self.player.dashing) > 40 and inimigo.estado != 'inativo':
                    inimigo.receber_dano(3)
            
            # Verifica se o inimigo caiu no limbo
            if inimigo.retangulo().y > self.limite_limbo_y and inimigo.estado != 'morto':
                print(f"Slime caiu no limbo! Posição Y: {inimigo.retangulo().y}")
                inimigo.vida = 0
                inimigo.estado = 'morto'
                if self.game:
                    self.game.tocar_som('matando_inimigo')
            
            # Remove inimigos mortos e conta
            if inimigo.estado == 'morto' and inimigo.animacao_morte_completa:
                self.inimigos_ativos.remove(inimigo)
                self.__retornar_inimigo_para_pool(inimigo)
                self.inimigos_mortos += 1
                print(f"Inimigo morto! Restam {self.get_inimigos_vivos()} inimigos.")
                
        
        # Não spawna novos inimigos - quantidade fixa
    
    def renderizar(self, surf, offset=(0, 0)):
        """Renderiza todos os inimigos"""
        for inimigo in self.inimigos_ativos:
            inimigo.renderizar(surf, offset)
    
    def render(self, surf, offset=(0, 0)):
        """Alias para renderizar - compatibilidade com o jogo"""
        self.renderizar(surf, offset)
    
    def verificar_colisao_projeteis(self, projeteis):
        """Verifica colisão entre projéteis e inimigos"""
        for projetil in projeteis[:]:
            if projetil.tipo == 'projetil':
                for inimigo in self.inimigos_ativos[:]:
                    if inimigo.estado != 'morto' and projetil.tipo == 'projetil' :
                        # Verifica colisão com hitbox mais precisa
                        projetil_rect = pygame.Rect(projetil.pos[0] + 8, projetil.pos[1] + 8, 16, 16)
                        inimigo_rect = pygame.Rect(inimigo.pos[0], inimigo.pos[1], 
                                                inimigo.tamanho[0], inimigo.tamanho[1])
                        
                        if projetil_rect.colliderect(inimigo_rect) and inimigo.estado != 'inativo':
                            # Remove projétil
                            if projetil in projeteis:
                                projeteis.remove(projetil)
                            
                            # Aplica 1 de dano ao inimigo (slime morre com 2 tiros)
                            vida_antes = inimigo.vida
                            inimigo.receber_dano(1)
                            
                            if self.player.furia < 100:
                                self.player.furia += 25
                            
                            # Se o inimigo morreu, toca som
                            if vida_antes > 0 and inimigo.vida <= 0:
                                if hasattr(self, '_SpawnManager__game') and self.game:
                                    self.game.tocar_som('matando_inimigo')
                                print(f"Slime morto por projétil!")
                            else:
                                print(f"Slime atingido! Vida restante: {inimigo.vida}")
                            
                            break  # Sai do loop de inimigos para este projétil
            elif projetil.tipo == 'osso':
                player_rect = self.player.retangulo()
                projetil_rect = pygame.Rect(projetil.pos[0] + 8, projetil.pos[1] + 8, 16, 16)
                if projetil_rect.colliderect(player_rect):
                    # Remove o projétil
                    if projetil in projeteis:
                        projeteis.remove(projetil)
                    # Aplica dano ao jogador
                    if hasattr(self.player, 'receber_dano'):
                        self.player.receber_dano(1, self.game)
                    # Opcional: tocar som ou efeito
                    if self.game:
                        self.game.tocar_som('dano_jogador')
                    print("Jogador atingido por projétil de esqueleto!")
                   

        
    
    def verificar_colisoes_projeteis(self, projeteis):
        """Alias para verificar_colisao_projeteis - compatibilidade com o jogo"""
        self.verificar_colisao_projeteis(projeteis)
    
    def get_inimigos_vivos(self):
        """Retorna o número de inimigos vivos"""
        return len([inimigo for inimigo in self.inimigos_ativos if inimigo.estado != 'morto'])
    
    def get_inimigos_mortos(self):
        """Retorna o número de inimigos mortos"""
        return self.inimigos_mortos
    
    def get_total_inimigos(self):
        """Retorna o total de inimigos no mapa"""
        return self.inimigos_totais
        
    def __verificar_colisao_player(self, inimigo):
        """Verifica se um inimigo está colidindo com o player"""
        inimigo_rect = inimigo.retangulo()
        player_rect = self.player.retangulo()
        
        return inimigo_rect.colliderect(player_rect)
    
    def todos_inimigos_mortos(self):
        """Verifica se todos os inimigos estão mortos"""
        return self.get_inimigos_vivos() == 0