import pygame
import random
from ..config import *

class ParticleEffect:
    def __init__(self, x, y, color, particle_count=10, lifetime=30):
        self.particles = []
        self.lifetime = lifetime
        
        for _ in range(particle_count):
            particle = {
                'pos': [x, y],
                'vel': [random.uniform(-2, 2), random.uniform(-2, 2)],
                'timer': lifetime,
                'color': color,
                'size': random.randint(2, 4)
            }
            self.particles.append(particle)
    
    def update(self):
        for particle in self.particles[:]:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['timer'] -= 1
            
            if particle['timer'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(
                surface,
                particle['color'],
                (int(particle['pos'][0]), int(particle['pos'][1])),
                particle['size']
            )

class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.load_animations()
    
    def load_animations(self):
        # Player animations
        self.animations['player_walk'] = self.load_spritesheet(
            ASSETS_DIR + 'knight.png',
            frame_width=64,
            frame_height=64,
            frames=4
        )
        
        # Enemy animations
        self.animations['enemy_attack'] = self.load_spritesheet(
            ASSETS_DIR + 'enemy-1.png',
            frame_width=64,
            frame_height=64,
            frames=4
        )
    
    def load_spritesheet(self, path, frame_width, frame_height, frames):
        try:
            spritesheet = pygame.image.load(path).convert_alpha()
            animation_frames = []
            
            for i in range(frames):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(spritesheet, (0, 0), 
                          (i * frame_width, 0, frame_width, frame_height))
                animation_frames.append(frame)
                
            return animation_frames
        except pygame.error:
            return None 