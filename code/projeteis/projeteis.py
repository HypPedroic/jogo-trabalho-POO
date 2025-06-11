# Importando as bibliotecas necessárias
import pygame
from utils.utils import load_images
from utils.animation import Animation


# Classe da entidade física
class Projetil:
    def __init__(self, pos, tamanho, movimento=[False, False]):
        self._assets = {
            'projetil': Animation(load_images('projeteis/flechaAzul'), img_dur=60),
        }
        self._pos = list(pos)
        self._tamanho = tamanho
        self._action = ''
        self._anim_offeset = (-32, -32)
        self._flip = False
        self._movimento = movimento  # [direita, esquerda]
        self.set_action('projetil')
        self.vidaMax = 1
        self.vida = self.vidaMax
        self._duracao = 60
        self._hit = False
    
    # Definindo property e setter para os atributos necessários    
    @property
    def assets(self):
        return self._assets
    
    @assets.setter
    def assets(self, value):
        self._assets = value
        
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def tamanho(self):
        return self._tamanho

    @tamanho.setter
    def tamanho(self, value):
        self._tamanho = value

    @property
    def action(self):
        return self._action
    
    @action.setter
    def action(self, value):
        self._action = value
    
    @property
    def anim_offeset(self):
        return self._anim_offeset
    
    @anim_offeset.setter
    def anim_offeset(self, value):
        self._anim_offeset = value
    
    @property
    def flip(self):
        return self._flip
    
    @flip.setter
    def flip(self, value):
        self._flip = value

    @property
    def movimento(self):
        return self._movimento

    @movimento.setter
    def movimento(self, value):
        self._movimento = value
    
    def mover_direita(self, estado=True):
        self._movimento[0] = estado

    def mover_esquerda(self, estado=True):
        self._movimento[1] = estado
    
    # Definindo os métodos necessários para movimentação, física e renderização 
    
    # Método para gerar o retângulo de colisão da entidade
    def retangulo(self):
        # Cria uma caixa de colisão menor e centralizada
        offset_x = 0
        offset_y = 0
        return pygame.Rect(self._pos[0] + offset_x, self._pos[1] + offset_y, 16, self._tamanho[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.assets[action].copy()

    # Método que vai atuar na movimentação da entidade e na física   
    def update(self, game, tilemap):
        #Reseta as colisões

        self.movimentar_X(game, tilemap)

        self.animation.update()
        
        self.set_action('projetil')

    def movimentar_X(self, game, tilemap):
        movimento_x = self.movimento[0] - self.movimento[1]

        self._pos[0] += movimento_x * 6
        # Verifica se a entidade está colidindo com algum retângulo de colisão para o eixo X
        self.colisao_X(game, tilemap, movimento_x)

        if movimento_x > 0:
            self._flip = False
        elif movimento_x < 0:
            self._flip = True

    def colisao_X(self, game, tilemap, movimento):
        retangulo_colisao = self.retangulo()
        for rect in tilemap.fisica_rect_around(self._pos):
            if retangulo_colisao.colliderect(rect):
                if movimento > 0:
                    retangulo_colisao.right = rect.left
                    self.vida = 0
                    self.hit = True
                if movimento < 0:
                    retangulo_colisao.left = rect.right
                    self.hit = True
                    self.vida = 0
                self._pos[0] = retangulo_colisao.x
        
        for inimigos in game.inimigos:
            if inimigos.retangulo().colliderect(retangulo_colisao):
                if movimento > 0:
                    retangulo_colisao.right = inimigos.retangulo().left
                    self.vida = 0
                    self.hit = True
                if movimento < 0:
                    retangulo_colisao.left = inimigos.retangulo().right
                    self.hit = True
                    self.vida = 0
                self._pos[0] = retangulo_colisao.x
                


    # Método que vai renderizar a entidade na tela
    def renderizar(self, surf, offset=(0, 0)):
        # Renderiza a entidade na tela
        surf.blit(pygame.transform.flip(self.animation.img(), self._flip, False), (self.pos[0] - offset[0] + self.anim_offeset[0], self.pos[1] - offset[1] + self.anim_offeset[1]))
        #surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
