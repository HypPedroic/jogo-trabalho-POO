# Importando as bibliotecas necessárias
import pygame
import random
from .slime import Slime

class SpawnManager:
    def __init__(self, tilemap, player):
        self.tilemap = tilemap
        self.player = player
        self.inimigos = []
        self.max_inimigos = 5
        self.posicoes_spawn = []
        self.tempo_spawn = 0
        self.intervalo_spawn = 300  # 5 segundos entre spawns
        
        # Calcula posições válidas de spawn
        self.calcular_posicoes_spawn()
        
        # Spawna inimigos iniciais
        self.spawn_inimigos_iniciais()
    
    def calcular_posicoes_spawn(self):
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
    
    def spawn_inimigo(self):
        """Spawna novos inimigos em posições aleatórias válidas"""
        if not self.posicoes_spawn:
            self.calcular_posicoes_spawn()
        
        if not self.posicoes_spawn:
            print("Nenhuma posição de spawn válida encontrada")
            return
        
        if len(self.inimigos) >= self.max_inimigos:
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
            for inimigo in self.inimigos:
                distancia_inimigo = ((pos_spawn[0] - inimigo.pos[0]) ** 2 + 
                                   (pos_spawn[1] - inimigo.pos[1]) ** 2) ** 0.5
                if distancia_inimigo < 150:
                    muito_perto = True
                    break
            
            if not muito_perto:
                # Cria novo slime
                novo_slime = Slime(pos_spawn, (16, 16))
                self.inimigos.append(novo_slime)
                print(f"Slime spawnado em {pos_spawn}")
                return
            
            tentativas += 1
        
        print("Não foi possível encontrar posição válida para spawn")
    
    def spawn_inimigos_iniciais(self):
        """Spawna os inimigos iniciais"""
        for _ in range(self.max_inimigos):
            self.spawn_inimigo()
        print("Inimigos iniciais spawnados!")
    
    def update(self):
        """Atualiza todos os inimigos"""
        for inimigo in self.inimigos[:]:
            inimigo.update(self.tilemap, self.player)
            
            # Verifica colisão com o player
            if inimigo.estado != 'morto' and self.verificar_colisao_player(inimigo):
                if inimigo.pode_atacar_jogador():
                    inimigo.atacar_jogador()
                    # Player recebe dano
                    self.player.receber_dano(inimigo.dano)
            
            # Remove inimigos mortos
            if inimigo.estado == 'morto' and inimigo.animacao_morte_completa:
                self.inimigos.remove(inimigo)
        
        # Spawna novos inimigos se necessário
        self.tempo_spawn += 1
        if self.tempo_spawn >= self.intervalo_spawn and len(self.inimigos) < self.max_inimigos:
            self.spawn_inimigo()
            self.tempo_spawn = 0
    
    def renderizar(self, surf, offset=(0, 0)):
        """Renderiza todos os inimigos"""
        for inimigo in self.inimigos:
            inimigo.render(surf, offset)
    
    def render(self, surf, offset=(0, 0)):
        """Alias para renderizar - compatibilidade com o jogo"""
        self.renderizar(surf, offset)
    
    def verificar_colisao_projeteis(self, projeteis):
        """Verifica colisão entre projéteis e inimigos"""
        for projetil in projeteis[:]:
            for inimigo in self.inimigos[:]:
                if inimigo._estado != 'morto':
                    # Verifica colisão
                    projetil_rect = pygame.Rect(projetil.pos[0], projetil.pos[1], 8, 8)
                    inimigo_rect = pygame.Rect(inimigo.pos[0], inimigo.pos[1], 
                                             inimigo.tamanho[0], inimigo.tamanho[1])
                    
                    if projetil_rect.colliderect(inimigo_rect):
                        # Remove projétil
                        if projetil in projeteis:
                            projeteis.remove(projetil)
                        
                        # Aplica dano ao inimigo (instant kill)
                        inimigo.receber_dano(999)
                        print(f"Slime morto por projétil!")
    
    def verificar_colisoes_projeteis(self, projeteis):
        """Alias para verificar_colisao_projeteis - compatibilidade com o jogo"""
        self.verificar_colisao_projeteis(projeteis)
    
    def get_inimigos_vivos(self):
        """Retorna o número de inimigos vivos"""
        return len([inimigo for inimigo in self.inimigos if inimigo.estado != 'morto'])
        
    def verificar_colisao_player(self, inimigo):
        """Verifica se um inimigo está colidindo com o player"""
        inimigo_rect = inimigo.retangulo()
        player_rect = self.player.retangulo()
        
        return inimigo_rect.colliderect(player_rect)
    
    def todos_inimigos_mortos(self):
        """Verifica se todos os inimigos estão mortos"""
        return self.get_inimigos_vivos() == 0