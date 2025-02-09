import pygame
import os
import sys
from pygame import gfxdraw
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

def draw_knight(surface):
    """Draw a simple knight figure"""
    # Body
    pygame.draw.rect(surface, (192, 192, 192), (24, 16, 16, 32))
    # Head
    pygame.draw.circle(surface, (192, 192, 192), (32, 16), 8)
    # Sword
    pygame.draw.rect(surface, (169, 169, 169), (40, 8, 16, 4))
    # Shield
    pygame.draw.rect(surface, (139, 69, 19), (8, 16, 8, 16))

def draw_enemy(surface, color):
    """Draw a simple enemy figure"""
    # Body
    pygame.draw.rect(surface, color, (16, 16, 32, 32))
    # Eyes
    pygame.draw.circle(surface, (255, 0, 0), (24, 24), 4)
    pygame.draw.circle(surface, (255, 0, 0), (40, 24), 4)

def draw_civilian(surface):
    """Draw a simple civilian figure"""
    # Body
    pygame.draw.rect(surface, (0, 255, 255), (24, 16, 16, 32))
    # Head
    pygame.draw.circle(surface, (255, 223, 196), (32, 16), 8)

def generate_map_texture(base_color, detail_color, pattern_type):
    """Generate detailed map textures"""
    surface = pygame.Surface((800, 600))
    surface.fill(base_color)
    
    # Add pattern based on map type
    if pattern_type == 'grass':
        # Draw grass-like patterns
        for y in range(0, 600, 10):
            for x in range(0, 800, 10):
                if random.random() < 0.3:
                    pygame.draw.line(surface, detail_color, 
                                   (x, y), (x + 4, y - 4), 1)
    
    elif pattern_type == 'desert':
        # Draw sand dune patterns
        for y in range(0, 600, 20):
            for x in range(0, 800, 40):
                points = [
                    (x, y),
                    (x + 10, y - 5),
                    (x + 20, y),
                    (x + 30, y + 5),
                    (x + 40, y)
                ]
                pygame.draw.lines(surface, detail_color, False, points, 1)
    
    elif pattern_type == 'dungeon':
        # Draw stone brick patterns
        for y in range(0, 600, 30):
            for x in range(0, 800, 40):
                pygame.draw.rect(surface, detail_color, 
                               (x, y, 35, 25), 1)
    
    return surface

def generate_placeholder_images():
    # Initialize pygame
    pygame.init()
    
    # Create directories if they don't exist
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(os.path.join(IMAGES_DIR, 'maps'), exist_ok=True)
    os.makedirs(SOUNDS_DIR, exist_ok=True)
    
    # Generate character sprites (64x64 pixels)
    sprite_size = (64, 64)
    
    # Knight (player)
    knight_surface = pygame.Surface(sprite_size, pygame.SRCALPHA)
    draw_knight(knight_surface)
    pygame.image.save(knight_surface, os.path.join(IMAGES_DIR, 'knight.png'))
    
    # Enemy 1
    enemy1_surface = pygame.Surface(sprite_size, pygame.SRCALPHA)
    draw_enemy(enemy1_surface, (255, 0, 0))
    pygame.image.save(enemy1_surface, os.path.join(IMAGES_DIR, 'enemy-1.png'))
    
    # Enemy 2
    enemy2_surface = pygame.Surface(sprite_size, pygame.SRCALPHA)
    draw_enemy(enemy2_surface, (255, 128, 0))
    pygame.image.save(enemy2_surface, os.path.join(IMAGES_DIR, 'enemy-2.png'))
    
    # Civilian
    civilian_surface = pygame.Surface(sprite_size, pygame.SRCALPHA)
    draw_civilian(civilian_surface)
    pygame.image.save(civilian_surface, os.path.join(IMAGES_DIR, 'civilian-1.png'))
    
    # Generate map textures (800x600 pixels)
    maps_dir = os.path.join(IMAGES_DIR, 'maps')
    
    # Grass map
    grass_map = generate_map_texture((34, 139, 34), (0, 100, 0), 'grass')
    pygame.image.save(grass_map, os.path.join(maps_dir, 'grass_map.png'))
    
    # Desert map
    desert_map = generate_map_texture((238, 232, 170), (218, 165, 32), 'desert')
    pygame.image.save(desert_map, os.path.join(maps_dir, 'desert_map.png'))
    
    # Dungeon map
    dungeon_map = generate_map_texture((47, 47, 47), (169, 169, 169), 'dungeon')
    pygame.image.save(dungeon_map, os.path.join(maps_dir, 'dungeon_map.png'))
    
    print("Placeholder images generated successfully!")
    print(f"Images saved to: {IMAGES_DIR}")
    print("\nGenerated images:")
    print("- knight.png (player character)")
    print("- enemy-1.png (first enemy type)")
    print("- enemy-2.png (second enemy type)")
    print("- civilian-1.png (NPC)")
    print("\nGenerated maps:")
    print("- maps/grass_map.png")
    print("- maps/desert_map.png")
    print("- maps/dungeon_map.png")

if __name__ == "__main__":
    generate_placeholder_images() w