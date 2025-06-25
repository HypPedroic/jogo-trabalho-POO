
import pygame
from utils.utils import load_images
from utils.animation import Animation

class Particle:
    def __init__(self, p_type, pos, velocity=[0, 0], frame=0):
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.assets = {
            'dash': Animation(load_images('particles/dash'), img_dur=6, loop=False)
        }
        self.animation = self.assets[p_type].copy()
        self.animation.frame = frame
    
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