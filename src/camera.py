import pygame
from config import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
        # Camera smoothing
        self.smoothing = 0.1
        self.target_x = 0
        self.target_y = 0
    
    def apply(self, entity):
        """Returns entity's rect relative to camera"""
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        """Returns rect relative to camera"""
        return rect.move(self.camera.topleft)
    
    def update(self, target):
        """Update camera position to follow target"""
        # Calculate target position (center on target)
        self.target_x = -target.rect.centerx + SCREEN_WIDTH // 2
        self.target_y = -target.rect.centery + SCREEN_HEIGHT // 2
        
        # Smooth camera movement
        self.camera.x += (self.target_x - self.camera.x) * self.smoothing
        self.camera.y += (self.target_y - self.camera.y) * self.smoothing 