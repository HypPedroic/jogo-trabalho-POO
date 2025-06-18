# Importando as bibliotecas necessárias
import pygame



# Classe da entidade física
class Entidade:
    def __init__(self, assets, pos, tamanho):
        self.__assets = assets
        self.__pos = list(pos)
        self.__tamanho = tamanho
        self.__velocidade = [0, 0]
        self.__colisoes = {'cima': False, 'baixo': False, 'esquerda': False, 'direita': False}
        self.__action = ''
        self.__anim_offeset = (-8, 0)
        self.__flip = False
        self.__movimento = [False, False]  # [direita, esquerda]
        
        # Configuração de estados de animação
        self.__estados_animacao = {
            'idle': {'loop': True, 'next_state': None},
            'walk': {'loop': True, 'next_state': None},
            'attack': {'loop': False, 'next_state': 'idle'},
            'hurt': {'loop': False, 'next_state': 'idle'},
            'death': {'loop': False, 'next_state': None}
        }
        
        # Configura as transições de estado inicial
        self.__configurar_transicoes_animacao()
        self.set_action('idle')
    
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
    def velocidade(self):
        return self.__velocidade

    @velocidade.setter
    def velocidade(self, value):
        self.__velocidade = value

    @property
    def colisoes(self):
        return self.__colisoes
    
    @colisoes.setter
    def colisoes(self, value):
        self.__colisoes = value

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
    
    def mover_direita(self, estado=True):
        self.__movimento[0] = estado

    def mover_esquerda(self, estado=True):
        self.__movimento[1] = estado
    
    def __configurar_transicoes_animacao(self):
        """Configura as transições entre estados de animação"""
        for estado, config in self.__estados_animacao.items():
            if estado in self.__assets:
                self.__assets[estado].loop = config['loop']
                if config['next_state']:
                    self.__assets[estado].add_state_transition(estado, config['next_state'])
    
    def set_action(self, action):
        """Define a ação atual e configura a animação apropriada"""
        if action != self.__action and action in self.__assets:
            self.__action = action
            self.__assets[self.__action].reset()
    
    # Definindo os métodos necessários para movimentação, física e renderização
    
    # Método para gerar o retângulo de colisão da entidade
    def retangulo(self):
        # Cria uma caixa de colisão menor e centralizada
        offset_x = 0
        offset_y = 0
        return pygame.Rect(self.__pos[0] + offset_x, self.__pos[1] + offset_y, 16, self.__tamanho[1])

    def set_action(self, action):
        if action != self.__action:
            self.__action = action
            self.animation = self.__assets[action].copy()

    # Método que vai atuar na movimentação da entidade e na física   
    def update(self, tilemap):
        #Reseta as colisões
        self.__colisoes = {'cima': False, 'baixo': False, 'esquerda': False, 'direita': False}

        self.__movimentar_X(tilemap)
        self.__movimentar_Y(tilemap)

        self.animation.update()

    def __movimentar_X(self, tilemap):
        movimento_x = self.__movimento[0] - self.__movimento[1]
        frame_movement = (movimento_x + self.__velocidade[0])

        self.__pos[0] += frame_movement * 3
        # Verifica se a entidade está colidindo com algum retângulo de colisão para o eixo X
        self.__colisao_X(tilemap, frame_movement)
            
        if movimento_x > 0:
            self.__flip = False
        elif movimento_x < 0:
            self.__flip = True

    def __movimentar_Y(self, tilemap):
        self.__pos[1] += self.__velocidade[1]
        # Verifica se a entidade está colidindo com algum retângulo de colisão para o eixo Y
        self.fisica_colisao_Y(tilemap)

    def __colisao_X(self, tilemap, movimento):
        retangulo_colisao = self.retangulo()
        for rect in tilemap.fisica_rect_around(self.__pos):
            if retangulo_colisao.colliderect(rect):
                if movimento > 0:
                    retangulo_colisao.right = rect.left
                    self.__colisoes['direita'] = True
                if movimento < 0:
                    retangulo_colisao.left = rect.right
                    self.__colisoes['esquerda'] = True
                self.__pos[0] = retangulo_colisao.x

    def fisica_colisao_Y(self, tilemap):
        retangulo_colisao = self.retangulo()
        for rect in tilemap.fisica_rect_around(self.__pos):
            if retangulo_colisao.colliderect(rect):
                if self.__velocidade[1] > 0:
                    retangulo_colisao.bottom = rect.top
                    self.__colisoes['baixo'] = True
                if self.__velocidade[1] < 0:
                    retangulo_colisao.top = rect.bottom
                    self.__colisoes['cima'] = True
                self.__pos[1] = retangulo_colisao.y

        self.__velocidade[1] = min(self.__velocidade[1]+0.15, 4)
        if self.__colisoes['cima'] or self.__colisoes['baixo']:
            self.__velocidade[1] = 0

    # Método que vai renderizar a entidade na tela
    def renderizar(self, surf, offset=(0, 0)):
        # Renderiza a entidade na tela
        surf.blit(pygame.transform.flip(self.animation.img(), self.__flip, False), (self.__pos[0] - offset[0] + self.__anim_offeset[0], self.__pos[1] - offset[1] + self.__anim_offeset[1]))
        #surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))



       
        
    