import pygame
import os
import sys
from pygame import gfxdraw

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

def generate_terrain_texture(color, pattern_type):
    """Generate terrain texture with patterns"""
    surface = pygame.Surface((800, 600))
    surface.fill(color)
    
    # Add pattern based on terrain type
    if pattern_type == 'sea':
        for y in range(0, 600, 20):
            for x in range(0, 800, 20):
                pygame.draw.circle(surface, (0, 0, 200), (x, y), 2)
    elif pattern_type == 'desert':
        for y in range(0, 600, 30):
            for x in range(0, 800, 30):
                pygame.draw.circle(surface, (200, 180, 100), (x, y), 3)
    else:  # hellscape
        for y in range(0, 600, 25):
            for x in range(0, 800, 25):
                pygame.draw.rect(surface, (180, 0, 0), (x, y, 5, 5))
    
    return surface

def generate_placeholder_images():
    # Initialize pygame
    pygame.init()
    
    # Create directories if they don't exist
    os.makedirs(IMAGES_DIR, exist_ok=True)
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
    
    # Generate terrain textures (800x600 pixels)
    # Sea
    sea_surface = generate_terrain_texture((0, 0, 255), 'sea')
    pygame.image.save(sea_surface, os.path.join(IMAGES_DIR, 'sea.png'))
    
    # Desert
    desert_surface = generate_terrain_texture((255, 223, 128), 'desert')
    pygame.image.save(desert_surface, os.path.join(IMAGES_DIR, 'desert.png'))
    
    # Hellscape
    hellscape_surface = generate_terrain_texture((255, 0, 0), 'hellscape')
    pygame.image.save(hellscape_surface, os.path.join(IMAGES_DIR, 'hellscape.png'))
    
    print("Placeholder images generated successfully!")
    print(f"Images saved to: {IMAGES_DIR}")
    print("\nGenerated images:")
    print("- knight.png (player character)")
    print("- enemy-1.png (first enemy type)")
    print("- enemy-2.png (second enemy type)")
    print("- civilian-1.png (NPC)")
    print("- sea.png (water terrain)")
    print("- desert.png (desert terrain)")
    print("- hellscape.png (damaged urban terrain)")

if __name__ == "__main__":
    generate_placeholder_images() 