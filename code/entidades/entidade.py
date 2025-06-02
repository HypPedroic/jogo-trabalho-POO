# Importando as bibliotecas necessárias
import pygame



# Classe da entidade física
class Entidade:
    def __init__(self, assets, pos, tamanho):
        self._assets = assets
        self._pos = list(pos)
        self._tamanho = tamanho
        self._velocidade = [0, 0]
        self._colisoes = {'cima': False, 'baixo': False, 'esquerda': False, 'direita': False}
        self._action = ''
        self._anim_offeset = (-8, 0)
        self._flip = False
        self._movimento = [False, False]  # [direita, esquerda]
        self.set_action('idle')
    
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
    def velocidade(self):
        return self._velocidade

    @velocidade.setter
    def velocidade(self, value):
        self._velocidade = value

    @property
    def colisoes(self):
        return self._colisoes
    
    @colisoes.setter
    def colisoes(self, value):
        self._colisoes = value

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
    def update(self, tilemap):
        #Reseta as colisões
        self._colisoes = {'cima': False, 'baixo': False, 'esquerda': False, 'direita': False}

        #Calcula o movimento da entidade baseado no estado atual
        movimento_x = self._movimento[0] - self._movimento[1]
        frame_movement = (movimento_x + self._velocidade[0], self._velocidade[1])

        self._pos[0] += frame_movement[0] * 3
        # Verifica se a entidade está colidindo com algum retângulo de colisão para o eixo X
        retangulo_colisao = self.retangulo()
        for rect in tilemap.fisica_rect_around(self._pos):
            if retangulo_colisao.colliderect(rect):
                if frame_movement[0] > 0:
                    retangulo_colisao.right = rect.left
                    self._colisoes['direita'] = True
                if frame_movement[0] < 0:
                    retangulo_colisao.left = rect.right
                    self._colisoes['esquerda'] = True
                self._pos[0] = retangulo_colisao.x

        self._pos[1] += frame_movement[1]
        # Verifica se a entidade está colidindo com algum retângulo de colisão para o eixo Y
        retangulo_colisao = self.retangulo()
        for rect in tilemap.fisica_rect_around(self._pos):
            if retangulo_colisao.colliderect(rect):
                if frame_movement[1] > 0:
                    retangulo_colisao.bottom = rect.top
                    self._colisoes['baixo'] = True
                if frame_movement[1] < 0:
                    retangulo_colisao.top = rect.bottom
                    self._colisoes['cima'] = True
                self._pos[1] = retangulo_colisao.y

        if movimento_x > 0:
            self._flip = False
        elif movimento_x < 0:
            self._flip = True

        #Gera a gravidade, movimento de queda
        #Gera a velocidade de queda e defina um limite para ela
        self.velocidade[1] = min(self.velocidade[1]+0.2, 5)
        #Se a entidade está colidindo com o chão, a velocidade de queda é 0
        if self.colisoes['cima'] or self.colisoes['baixo']:
            self.velocidade[1] = 0

        self.animation.update()

    # Método que vai renderizar a entidade na tela
    def renderizar(self, surf, offset=(0, 0)):
        # Renderiza a entidade na tela
        surf.blit(pygame.transform.flip(self.animation.img(), self._flip, False), (self.pos[0] - offset[0] + self.anim_offeset[0], self.pos[1] - offset[1] + self.anim_offeset[1]))
        #surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))



       
        
    