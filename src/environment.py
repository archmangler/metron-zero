import pygame
import random
from config import *
import os

class Terrain(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, terrain_type):
        super().__init__()
        self.terrain_type = terrain_type
        
        try:
            # Load terrain texture based on type
            if terrain_type == 'sea':
                self.image = pygame.image.load(os.path.join(IMAGES_DIR, 'sea.png')).convert_alpha()
            elif terrain_type == 'desert':
                self.image = pygame.image.load(os.path.join(IMAGES_DIR, 'desert.png')).convert_alpha()
            else:  # hellscape
                self.image = pygame.image.load(os.path.join(IMAGES_DIR, 'hellscape.png')).convert_alpha()
            
            # Scale image to chunk size
            self.image = pygame.transform.scale(self.image, (width, height))
            
        except (pygame.error, FileNotFoundError):
            # Create fallback colored surface if image loading fails
            self.image = pygame.Surface((width, height))
            if terrain_type == 'sea':
                self.image.fill((0, 0, 255))  # Blue for sea
            elif terrain_type == 'desert':
                self.image.fill((255, 223, 128))  # Sand color for desert
            else:
                self.image.fill((255, 0, 0))  # Red for hellscape
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Collision mask for precise collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
        # Movement penalty for this terrain type
        self.movement_penalty = TERRAIN_MOVEMENT_PENALTIES.get(terrain_type, 1.0)

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
        
        # Terrain generation parameters
        self.chunk_size = CHUNK_SIZE
        self.num_chunks_x = screen_width // CHUNK_SIZE + 1
        self.num_chunks_y = screen_height // CHUNK_SIZE + 1
    
    def generate_terrain(self):
        for y in range(self.num_chunks_y):
            for x in range(self.num_chunks_x):
                # Determine terrain type based on position or noise
                terrain_type = self.determine_terrain_type(x, y)
                
                # Create terrain chunk
                terrain = Terrain(
                    x * self.chunk_size,
                    y * self.chunk_size,
                    self.chunk_size,
                    self.chunk_size,
                    terrain_type
                )
                
                self.terrain_grid.append(terrain)
                
                # Add obstacles based on terrain type
                if terrain_type == 'sea':
                    if random.random() < 0.2:  # 20% chance for rocks in sea
                        self.add_obstacle(x * self.chunk_size, y * self.chunk_size)
    
    def determine_terrain_type(self, x, y):
        # Simple terrain distribution for demonstration
        if y < self.num_chunks_y // 3:
            return 'sea'
        elif y < (self.num_chunks_y * 2) // 3:
            return 'desert'
        else:
            return 'hellscape'
    
    def add_obstacle(self, x, y):
        obstacle = pygame.sprite.Sprite()
        obstacle.image = pygame.Surface((20, 20))
        obstacle.image.fill((100, 100, 100))  # Gray color for obstacles
        obstacle.rect = obstacle.image.get_rect()
        obstacle.rect.x = x + random.randint(0, self.chunk_size - 20)
        obstacle.rect.y = y + random.randint(0, self.chunk_size - 20)
        self.obstacles.add(obstacle)
    
    def get_terrain_at_position(self, x, y):
        for terrain in self.terrain_grid:
            if terrain.rect.collidepoint(x, y):
                return terrain.terrain_type
        return 'default' 
