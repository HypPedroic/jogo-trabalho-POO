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
        self.__anim_offeset = [0, 0]
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
        self.configurar_transicoes_animacao()
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
        
    @property
    def estados_animacao(self):
        return self.__estados_animacao

    @estados_animacao.setter
    def estados_animacao(self, value):
        self.__estados_animacao = value

    @property
    def animation(self):
        return self.__animation

    @animation.setter
    def animation(self, value):
        self.__animation = value
    
    def mover_direita(self, estado=True):
        self.movimento[0] = estado

    def mover_esquerda(self, estado=True):
        self.movimento[1] = estado
    
    def configurar_transicoes_animacao(self):
        """Configura as transições entre estados de animação"""
        for estado, config in self.estados_animacao.items():
            if estado in self.assets:
                self.assets[estado].loop = config['loop']
                if config['next_state']:
                    self.assets[estado].add_state_transition(estado, config['next_state'])
    
    def set_action(self, action):
        """Define a ação atual e configura a animação apropriada"""
        if action != self.action and action in self.assets:
            self.action = action
            self.assets[self.action].reset()
    
    # Definindo os métodos necessários para movimentação, física e renderização
    
    # Método para gerar o retângulo de colisão da entidade
    def retangulo(self):
        # Cria uma caixa de colisão menor e centralizada
        offset_x = 0
        offset_y = 0
        return pygame.Rect(self.pos[0] + offset_x, self.pos[1] + offset_y, 16, self.tamanho[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.assets[action].copy()

    # Método que vai atuar na movimentação da entidade e na física   
    def update(self, tilemap):
        #Reseta as colisões
        self.colisoes = {'cima': False, 'baixo': False, 'esquerda': False, 'direita': False}

        self.movimentar_X(tilemap)
        self.movimentar_Y(tilemap)

        self.animation.update()

    def movimentar_X(self, tilemap):
        movimento_x = self.movimento[0] - self.movimento[1]
        frame_movement = (movimento_x + self.velocidade[0])

        self.pos[0] += frame_movement * 2
        # Verifica se a entidade está colidindo com algum retângulo de colisão para o eixo X
        self.colisao_X(tilemap, frame_movement)
            
        if movimento_x > 0:
            self.flip = False
        elif movimento_x < 0:
            self.flip = True

    def movimentar_Y(self, tilemap):
        self.pos[1] += self.velocidade[1]
        # Verifica se a entidade está colidindo com algum retângulo de colisão para o eixo Y
        self.fisica_colisao_Y(tilemap)

    def colisao_X(self, tilemap, movimento):
        retangulo_colisao = self.retangulo()
        for rect in tilemap.fisica_rect_around(self.pos):
            if retangulo_colisao.colliderect(rect):
                if movimento > 0:
                    retangulo_colisao.right = rect.left
                    self.colisoes['direita'] = True
                if movimento < 0:
                    retangulo_colisao.left = rect.right
                    self.colisoes['esquerda'] = True
                self.pos[0] = retangulo_colisao.x

    def fisica_colisao_Y(self, tilemap):
        retangulo_colisao = self.retangulo()
        for rect in tilemap.fisica_rect_around(self.pos):
            if retangulo_colisao.colliderect(rect):
                if self.velocidade[1] > 0:
                    retangulo_colisao.bottom = rect.top
                    self.colisoes['baixo'] = True
                if self.velocidade[1] < 0:
                    retangulo_colisao.top = rect.bottom
                    self.colisoes['cima'] = True
                self.pos[1] = retangulo_colisao.y

        self.velocidade[1] = min(self.velocidade[1]+0.15, 4)
        if self.colisoes['cima'] or self.colisoes['baixo']:
            self.velocidade[1] = 0

    # Método que vai renderizar a entidade na tela
    def renderizar(self, surf, offset=(0, 0)):
        # Renderiza a entidade na tela
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offeset[0], self.pos[1] - offset[1] + self.anim_offeset[1]))
        #surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))



       
        
    