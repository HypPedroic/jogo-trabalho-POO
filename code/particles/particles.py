
import pygame
from utils.utils import load_images
from animation.animation import Animation

class Particle:
    def __init__(self, p_type, pos, velocity=[0, 0], frame=0):
        self.__type = p_type
        self.__pos = list(pos)
        self.__velocity = list(velocity)
        self.__assets = {
            'dash': Animation(load_images('particles/dash'), img_dur=6, loop=False)
        }
        self.__animation = self.assets[p_type].copy()
        self.__animation.frame = frame
        
    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, value):
        self.__velocity = value

    @property
    def assets(self):
        return self.__assets

    @assets.setter
    def assets(self, value):
        self.__assets = value

    @property
    def animation(self):
        return self.__animation

    @animation.setter
    def animation(self, value):
        self.__animation = value
    
    def update(self):
        kill = False
        if self.animation.done:
            kill = True
        
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        self.animation.update()
        
        return kill
    
    def render(self, surf, offset=(0, 0)):
        img = self.animation.img()
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))