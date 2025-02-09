import pygame
import random
from config import *

class TerrainObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))  # Gray color for obstacles
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

class TerrainManager:
    def __init__(self):
        self.terrain_map = {}
        self.obstacles = pygame.sprite.Group()
        self.generate_terrain()
        self.generate_obstacles()
        
    def generate_terrain(self):
        """Generate simple terrain"""
        for x in range(-10, 11):
            for y in range(-10, 11):
                self.terrain_map[(x, y)] = 'sea'
    
    def generate_obstacles(self):
        """Generate random obstacles"""
        # Clear existing obstacles
        self.obstacles.empty()
        
        # Generate new obstacles
        for _ in range(20):  # Generate 20 random obstacles
            x = random.randint(-1000, 1000)
            y = random.randint(-1000, 1000)
            width = random.randint(50, 150)
            height = random.randint(50, 150)
            
            obstacle = TerrainObstacle(x, y, width, height)
            self.obstacles.add(obstacle)
    
    def get_terrain_at_position(self, x, y):
        """Get terrain type at world position"""
        chunk_x = int(x // CHUNK_SIZE)
        chunk_y = int(y // CHUNK_SIZE)
        return self.terrain_map.get((chunk_x, chunk_y), 'sea')
    
    def draw(self, screen, camera):
        """Draw terrain and obstacles"""
        # Draw terrain chunks
        cam_x = -camera.camera.x
        cam_y = -camera.camera.y
        
        start_x = int((cam_x - CHUNK_SIZE) // CHUNK_SIZE)
        end_x = int((cam_x + SCREEN_WIDTH + CHUNK_SIZE) // CHUNK_SIZE)
        start_y = int((cam_y - CHUNK_SIZE) // CHUNK_SIZE)
        end_y = int((cam_y + SCREEN_HEIGHT + CHUNK_SIZE) // CHUNK_SIZE)
        
        # Draw terrain
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                screen_x = x * CHUNK_SIZE + camera.camera.x
                screen_y = y * CHUNK_SIZE + camera.camera.y
                pygame.draw.rect(screen, (0, 0, 255), 
                               (screen_x, screen_y, CHUNK_SIZE, CHUNK_SIZE))
                pygame.draw.rect(screen, (255, 255, 255), 
                               (screen_x, screen_y, CHUNK_SIZE, CHUNK_SIZE), 1)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            screen_pos = camera.apply(obstacle)
            if screen.get_rect().colliderect(screen_pos):
                screen.blit(obstacle.image, screen_pos)