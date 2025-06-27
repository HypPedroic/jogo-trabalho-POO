# Importando as bibliotecas necessárias
import pygame
from utils.utils import load_images
from animation.animation import Animation


# Classe da entidade física
class Projetil:
    def __init__(self, pos, tamanho, movimento=[False, False], tipo='projetil'):
        self.__assets = {
            'projetil': Animation(load_images('projeteis/flechaAzul'), img_dur=60),
            'osso': Animation(load_images('projeteis/osso'), img_dur=60),
        }
        self.__pos = list(pos)
        self.__tamanho = tamanho
        self.__action = ''
        self.__anim_offeset = (-32, -32)
        self.__flip = False
        self.__movimento = movimento  # [direita, esquerda]
        self.__set_action('projetil')
        self.__vidaMax = 1
        self.__vida = self.__vidaMax
        self.__tipo = tipo
        
        if self.__tipo == 'projetil':
            self.__duracao = 120  # Projéteis do player duram mais
        else:
            self.__duracao = 60   # Projéteis dos inimigos mantêm duração original
        
        if self.__tipo == 'projetil':
            self.__anim_offeset = (-32, -32)
            self.__velocidade = 10
        elif self.__tipo == 'osso':
            self.__anim_offeset = (0, 0)
            self.__velocidade = 4

    # Definindo property e setter para os atributos necessários    
    @property
    def assets(self):
        return self.__assets
    
    @assets.setter
    def assets(self, value):
        self.__assets = value
        
    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value

    @property
    def tamanho(self):
        return self.__tamanho

    @tamanho.setter
    def tamanho(self, value):
        self.__tamanho = value

    @property
    def action(self):
        return self.__action
    
    @action.setter
    def action(self, value):
        self.__action = value
    
    @property
    def anim_offeset(self):
        return self.__anim_offeset
    
    @anim_offeset.setter
    def anim_offeset(self, value):
        self.__anim_offeset = value
    
    @property
    def flip(self):
        return self.__flip
    
    @flip.setter
    def flip(self, value):
        self.__flip = value

    @property
    def movimento(self):
        return self.__movimento

    @movimento.setter
    def movimento(self, value):
        self.__movimento = value
    
    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, value):
        self.__vida = value
    
    @property
    def vidaMax(self):
        return self.__vidaMax
    
    @vidaMax.setter
    def vidaMax(self, value):
        self.__vidaMax = value
        
    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, value):
        self.__tipo = value
        
    @property
    def velocidade(self):
        return self.__velocidade
    
    @velocidade.setter
    def velocidade(self, value):
        self.__velocidade = value
        
    @property
    def duracao(self):
        return self.__duracao
    
    @duracao.setter
    def duracao(self, value):
        self.__duracao = value
    
    def mover_direita(self, estado=True):
        self.__movimento[0] = estado

    def mover_esquerda(self, estado=True):
        self.__movimento[1] = estado

    # Definindo os métodos necessários para movimentação, física e renderização
    
    # Método para gerar o retângulo de colisão da entidade
    def retangulo(self):
        # Cria uma caixa de colisão menor e centralizada
        offset_x = 0
        offset_y = 0
        return pygame.Rect(self.__pos[0] + offset_x, self.__pos[1] + offset_y, 16, self.__tamanho[1])

    def __set_action(self, action):
        if action != self.__action:
            self.__action = action
            self.__animation = self.__assets[action].copy()

    # Método que vai atuar na movimentação da entidade e na física   
    def update(self, game, tilemap):
        #Reseta as colisões
        
        # Decrementa a duração do projétil
        self.__duracao -= 1
        if self.__duracao <= 0:
            self.__vida = 0  # Remove o projétil quando a duração acaba

        self.__movimentar_X(game, tilemap)

        self.__animation.update()
        
        self.__set_action(self.tipo)

    def __movimentar_X(self, game, tilemap):
        movimento_x = self.__movimento[0] - self.__movimento[1]

        self.__pos[0] += movimento_x * self.velocidade
        # Verifica se a entidade está colidindo com algum retângulo de colisão para o eixo X
        self.__colisao_X(game, tilemap, movimento_x)

        if movimento_x > 0:
            self.__flip = False
        elif movimento_x < 0:
            self.__flip = True

    def __colisao_X(self, game, tilemap, movimento):
        retangulo_colisao = self.retangulo()
        for rect in tilemap.fisica_rect_around(self.__pos):
            if retangulo_colisao.colliderect(rect):
                if movimento > 0:
                    retangulo_colisao.right = rect.left
                    self.__vida = 0
                    self.__hit = True
                if movimento < 0:
                    retangulo_colisao.left = rect.right
                    self.__hit = True
                    self.__vida = 0
                self.__pos[0] = retangulo_colisao.x
        

                


    # Método que vai renderizar a entidade na tela
    def renderizar(self, surf, offset=(0, 0)):
        # Renderiza a entidade na tela
        surf.blit(pygame.transform.flip(self.__animation.img(), self.__flip, False), (self.__pos[0] - offset[0] + self.__anim_offeset[0], self.__pos[1] - offset[1] + self.__anim_offeset[1]))
        #surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
