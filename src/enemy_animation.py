import pygame
import os
from config import *

class EnemyAnimation:
    def __init__(self, enemy_type="enemy1", frame_width=93, frame_height=93):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.enemy_type = enemy_type
        self.animations = {
            'idle': [],
            'walk': [],
            'attack': []
        }
        self.current_state = 'idle'
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 100  # milliseconds between frames
        self.facing_right = True
        
        self.load_sprite_sheets()
    
    def load_sprite_sheets(self):
        base_path = os.path.join(ENEMY_ASSETS_DIR, self.enemy_type)
        
        # Load animations for each state
        for state in self.animations.keys():
            try:
                sprite_sheet = pygame.image.load(
                    os.path.join(base_path, f"{state}.png")
                ).convert_alpha()
                self.animations[state] = self.extract_frames(sprite_sheet)
                print(f"Loaded {len(self.animations[state])} frames for {self.enemy_type} {state}")
            except (pygame.error, FileNotFoundError) as e:
                print(f"Error loading {self.enemy_type} {state} animation: {e}")
                self.create_placeholder_frames(state)
    
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
    
    def create_placeholder_frames(self, state, num_frames=4):
        """Create placeholder frames for missing animations"""
        frames = []
        colors = {
            'idle': (255, 0, 0),     # Red
            'walk': (0, 255, 0),     # Green
            'attack': (255, 255, 0)  # Yellow
        }
        
        for _ in range(num_frames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            pygame.draw.rect(frame, colors.get(state, (128, 128, 128)), 
                           (0, 0, self.frame_width, self.frame_height))
            frames.append(frame)
        
        self.animations[state] = frames
        print(f"Created {num_frames} placeholder frames for {self.enemy_type} {state}")
    
    def update(self, dt, state=None, moving=False):
        if state and state in self.animations:
            self.current_state = state
        
        if self.animations[self.current_state]:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                num_frames = len(self.animations[self.current_state])
                self.current_frame = (self.current_frame + 1) % num_frames
    
    def get_current_frame(self):
        frames = self.animations[self.current_state]
        if not frames:
            self.create_placeholder_frames(self.current_state)
            frames = self.animations[self.current_state]
        
        # Ensure current_frame is within bounds
        self.current_frame = min(self.current_frame, len(frames) - 1)
        frame = frames[self.current_frame]
        
        # Flip the frame if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        
        return frame 