import pygame
import os
from config import *  # Add this to get access to IMAGES_DIR

class DirectionalAnimation:
    def __init__(self, frame_width=93, frame_height=93):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.animations = {
            'right': [],
            'left': [],
            'up': [],
            'down': [],
        }
        self.current_direction = 'down'
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 100  # milliseconds between frames
        self.is_moving = False
        
        self.load_sprite_sheets()
        
        # Ensure we have at least one frame for each direction
        for direction in self.animations:
            if not self.animations[direction]:
                self.create_placeholder_frame(direction)
    
    def load_sprite_sheets(self):
        sprite_sheets = {
            'right': PLAYER_SPRITE_RIGHT,
            'left': PLAYER_SPRITE_LEFT,
            'up': PLAYER_SPRITE_UP,
            'down': PLAYER_SPRITE_DOWN
        }
        
        for direction, path in sprite_sheets.items():
            try:
                sheet = pygame.image.load(path).convert_alpha()
                self.animations[direction] = self.extract_frames(sheet)
                print(f"Loaded {len(self.animations[direction])} frames for {direction} direction")
            except (pygame.error, FileNotFoundError) as e:
                print(f"Error loading {direction} sprite sheet: {e}")
                self.create_placeholder_frame(direction)
    
    def extract_frames(self, sprite_sheet):
        frames = []
        sheet_width = sprite_sheet.get_width()
        num_frames = max(1, sheet_width // self.frame_width)
        
        for i in range(num_frames):
            frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame_surface.blit(sprite_sheet, (0, 0), 
                             (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frames.append(frame_surface)
        
        return frames
    
    def create_placeholder_frame(self, direction):
        """Create a single colored rectangle as placeholder for a direction"""
        colors = {
            'right': (255, 0, 0),    # Red
            'left': (0, 255, 0),     # Green
            'up': (0, 0, 255),       # Blue
            'down': (255, 255, 0)    # Yellow
        }
        
        frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        pygame.draw.rect(frame, colors.get(direction, (128, 128, 128)), 
                        (0, 0, self.frame_width, self.frame_height))
        self.animations[direction] = [frame]  # Single frame animation
        print(f"Created placeholder for {direction} direction")
    
    def update(self, dt, direction=None, is_moving=False):
        self.is_moving = is_moving
        
        if direction:
            self.current_direction = direction
        
        if self.is_moving and self.animations[self.current_direction]:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                num_frames = len(self.animations[self.current_direction])
                self.current_frame = (self.current_frame + 1) % num_frames
        else:
            # Reset to idle frame (first frame) when not moving
            self.current_frame = 0
    
    def get_current_frame(self):
        frames = self.animations[self.current_direction]
        if not frames:
            # If no frames available for current direction, create a placeholder
            self.create_placeholder_frame(self.current_direction)
            frames = self.animations[self.current_direction]
        
        # Ensure current_frame is within bounds
        self.current_frame = min(self.current_frame, len(frames) - 1)
        return frames[self.current_frame] 