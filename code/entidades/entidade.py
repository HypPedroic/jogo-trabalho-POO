# Importando as bibliotecas necessárias
import pygame



# Classe da entidade física
class Entidade:
    def __init__(self, game, e_tipo, pos, tamanho):
        self._game = game
        self._e_tipo = e_tipo
        self._pos = list(pos)
        self._tamanho = tamanho
        self._velocidade = [0, 0]
        self._colisoes = {'cima': False, 'baixo': False, 'esquerda': False, 'direita': False}
    
    # Definindo property e setter para os atributos necessários    
    @property
    def game(self):
        return self._game
    
    @game.setter
    def game(self, value):
        self._game = value
        
    @property
    def e_tipo(self):
        return self._e_tipo
    
    @e_tipo.setter
    def e_tipo(self, value):
        self._e_tipo = value
        
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
        
        
    # Definindo os métodos necessários para movimentação, física e renderização 
    
    # Método para gerar o retângulo de colisão da entidade
    def retangulo(self):
        return pygame.Rect(self._pos[0], self._pos[1], self._tamanho[0], self._tamanho[1])

    # Método que vai atuar na movimentação da entidade e na física   
    def update(self, movement):
        #Reseta as colisões
        self._colisoes = {'cima': False, 'baixo': False, 'esquerda': False, 'direita': False}

        #Calcula o movimento da entidade
        frame_movement = (movement[0] + self._velocidade[0], movement[1] + self._velocidade[1])

        self._pos[0] += frame_movement[0]
        # Verifica se a entidade está colidindo com algum retângulo de colisão para o eixo X
        retangulo_colisao = self.retangulo()
        for rect in self.game.tilemap.fisica_rect_around(self._pos):
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
        for rect in self.game.tilemap.fisica_rect_around(self._pos):
            if retangulo_colisao.colliderect(rect):
                if frame_movement[1] > 0:
                    retangulo_colisao.bottom = rect.top
                    self._colisoes['baixo'] = True
                if frame_movement[1] < 0:
                    retangulo_colisao.top = rect.bottom
                    self._colisoes['cima'] = True
                self._pos[1] = retangulo_colisao.y


        #Gera a gravidade, movimento de queda
        #Gera a velocidade de queda e defina um limite para ela
        self.velocidade[1] = min(self.velocidade[1]+0.2, 5)
        #Se a entidade está colidindo com o chão, a velocidade de queda é 0
        if self._colisoes['cima'] or self._colisoes['baixo']:
            self.velocidade[1] = 0


    # Método que vai renderizar a entidade na tela
    def renderizar(self, surf, offset=(0, 0)):
        # Renderiza a entidade na tela
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))



       
        
    