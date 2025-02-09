import pygame
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

def generate_placeholder_images():
    # Create directories if they don't exist
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(SOUNDS_DIR, exist_ok=True)
    
    # Initialize pygame
    pygame.init()
    
    # Generate background placeholders
    backgrounds = {
        'sea.png': (0, 0, 255),      # Blue
        'desert.png': (255, 223, 128),  # Sand color
        'hellscape.png': (255, 0, 0)    # Red
    }
    
    for name, color in backgrounds.items():
        surface = pygame.Surface((800, 600))
        surface.fill(color)
        pygame.image.save(surface, os.path.join(IMAGES_DIR, name))
    
    # Generate sprite placeholders
    sprites = {
        'knight.png': (0, 255, 0),    # Green
        'enemy-1.png': (255, 0, 0),   # Red
        'enemy-2.png': (255, 128, 0), # Orange
        'civilian-1.png': (255, 255, 0) # Yellow
    }
    
    for name, color in sprites.items():
        surface = pygame.Surface((64, 64))
        surface.fill(color)
        pygame.image.save(surface, os.path.join(IMAGES_DIR, name))
    
    print("Placeholder images generated successfully!")

if __name__ == "__main__":
    generate_placeholder_images() 