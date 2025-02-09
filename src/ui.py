import pygame
from config import *

class UI:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Health bar settings
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.health_bar_position = (20, 20)
        
        # Score settings
        self.score_position = (SCREEN_WIDTH - 150, 20)
        
        # Message settings
        self.message = ""
        self.message_timer = 0
        self.message_duration = 2000  # 2 seconds
    
    def update(self):
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= self.game.clock.get_time()
            if self.message_timer <= 0:
                self.message = ""
    
    def draw(self, screen):
        # Draw health bar
        self.draw_health_bar(screen)
        
        # Draw score
        self.draw_score(screen)
        
        # Draw message
        if self.message:
            self.draw_message(screen)
    
    def draw_health_bar(self, screen):
        # Background
        pygame.draw.rect(screen, (64, 64, 64), 
                        (*self.health_bar_position, self.health_bar_width, self.health_bar_height))
        
        # Health bar
        health_percentage = max(0, self.game.player.health / PLAYER_HEALTH)
        current_health_width = int(self.health_bar_width * health_percentage)
        
        # Health color (green to red based on health)
        health_color = (
            int(255 * (1 - health_percentage)),  # Red
            int(255 * health_percentage),        # Green
            0                                    # Blue
        )
        
        pygame.draw.rect(screen, health_color,
                        (*self.health_bar_position, current_health_width, self.health_bar_height))
        
        # Health text
        health_text = f"HP: {self.game.player.health}/{PLAYER_HEALTH}"
        text_surface = self.small_font.render(health_text, True, WHITE)
        text_rect = text_surface.get_rect(midleft=(self.health_bar_position[0] + 5, 
                                                  self.health_bar_position[1] + self.health_bar_height // 2))
        screen.blit(text_surface, text_rect)
    
    def draw_score(self, screen):
        score_text = f"Score: {getattr(self.game, 'score', 0)}"
        text_surface = self.font.render(score_text, True, WHITE)
        screen.blit(text_surface, self.score_position)
    
    def draw_message(self, screen):
        text_surface = self.font.render(self.message, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(text_surface, text_rect)
    
    def show_message(self, message, duration=2000):
        """Show a message for the specified duration (in milliseconds)"""
        self.message = message
        self.message_timer = duration
    
    def show_game_over(self):
        """Show game over screen"""
        text_surface = self.font.render("Game Over", True, RED)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.game.screen.blit(text_surface, text_rect)
        
        restart_text = self.small_font.render("Press SPACE to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.game.screen.blit(restart_text, restart_rect) 