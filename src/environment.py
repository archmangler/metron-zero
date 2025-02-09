import pygame
from config import *

class Terrain(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, terrain_type):
        super().__init__()
        self.terrain_type = terrain_type
        
        # Load appropriate terrain texture
        try:
            if terrain_type == 'sea':
                self.image = pygame.image.load(ASSETS_DIR + 'sea.png').convert_alpha()
            elif terrain_type == 'desert':
                self.image = pygame.image.load(ASSETS_DIR + 'desert.png').convert_alpha()
            elif terrain_type == 'hellscape':
                self.image = pygame.image.load(ASSETS_DIR + 'hellscape.png').convert_alpha()
            
            self.image = pygame.transform.scale(self.image, (width, height))
        except pygame.error:
            self.image = pygame.Surface((width, height))
            self.image.fill(BLUE if terrain_type == 'sea' else 
                          (255, 200, 100) if terrain_type == 'desert' else 
                          (100, 50, 50))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Terrain properties
        self.movement_penalty = self.get_movement_penalty()
        self.is_obstacle = terrain_type == 'sea'

    def get_movement_penalty(self):
        # Different terrain types affect movement speed
        if self.terrain_type == 'sea':
            return 0.5  # Slow in water
        elif self.terrain_type == 'desert':
            return 0.7  # Somewhat slow in sand
        else:
            return 1.0  # Normal speed on hellscape

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class TerrainManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.terrain_grid = []
        self.obstacles = pygame.sprite.Group()
        
    def generate_terrain(self):
        # Example terrain generation
        terrain_types = ['sea', 'desert', 'hellscape']
        chunk_size = 200
        
        for x in range(0, self.screen_width, chunk_size):
            for y in range(0, self.screen_height, chunk_size):
                terrain_type = terrain_types[(x + y) // chunk_size % len(terrain_types)]
                terrain = Terrain(x, y, chunk_size, chunk_size, terrain_type)
                self.terrain_grid.append(terrain)
        
        # Add some obstacles
        self.generate_obstacles()
    
    def generate_obstacles(self):
        # Example obstacle placement
        obstacle_positions = [
            (100, 100, 50, 50),
            (300, 300, 100, 20),
            (500, 400, 30, 100),
            (200, 500, 80, 80)
        ]
        
        for pos in obstacle_positions:
            obstacle = Obstacle(*pos)
            self.obstacles.add(obstacle)
    
    def get_terrain_at_position(self, x, y):
        for terrain in self.terrain_grid:
            if terrain.rect.collidepoint(x, y):
                return terrain
        return None 