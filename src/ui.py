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
        
        # Radar settings
        self.show_radar = True
        self.radar_size = 150
        self.radar_position = (20, 60)
        self.radar_scale = 0.1
        
        # Message settings
        self.message = ""
        self.message_timer = 0
        self.message_duration = 2000
    
    def update(self):
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= self.game.clock.get_time()
            if self.message_timer <= 0:
                self.message = ""
    
    def draw(self, screen):
        print("Drawing UI, radar status:", self.show_radar)  # Debug output
        
        # Draw radar first (so it's behind other UI elements)
        if self.show_radar:
            print("Drawing radar")  # Debug output
            # Create radar surface
            radar_surface = pygame.Surface((self.radar_size, self.radar_size))
            radar_surface.fill((0, 0, 0))  # Black background
            
            # Draw radar border
            pygame.draw.rect(radar_surface, (0, 255, 0), 
                           (0, 0, self.radar_size, self.radar_size), 2)  # Green border
            
            # Calculate radar center
            radar_center = (self.radar_size // 2, self.radar_size // 2)
            
            # Draw player position (center of radar)
            pygame.draw.circle(radar_surface, (0, 255, 0), radar_center, 4)  # Green dot for player
            
            # Draw enemies on radar
            for enemy in self.game.enemies:
                # Calculate relative position to player
                rel_x = enemy.rect.centerx - self.game.player.rect.centerx
                rel_y = enemy.rect.centery - self.game.player.rect.centery
                
                # Scale position to radar size
                radar_x = radar_center[0] + int(rel_x * self.radar_scale)
                radar_y = radar_center[1] + int(rel_y * self.radar_scale)
                
                # Check if enemy is within radar bounds
                if (0 <= radar_x < self.radar_size and 
                    0 <= radar_y < self.radar_size):
                    # Draw enemy dot
                    pygame.draw.circle(radar_surface, (255, 0, 0), 
                                     (radar_x, radar_y), 3)  # Red dot for enemies
            
            # Draw NPCs on radar
            try:
                for npc in self.game.npcs:  # Add NPCs to radar
                    # Calculate relative position to player
                    rel_x = npc.rect.centerx - self.game.player.rect.centerx
                    rel_y = npc.rect.centery - self.game.player.rect.centery
                    
                    # Scale position to radar size
                    radar_x = radar_center[0] + int(rel_x * self.radar_scale)
                    radar_y = radar_center[1] + int(rel_y * self.radar_scale)
                    
                    # Check if NPC is within radar bounds
                    if (0 <= radar_x < self.radar_size and 
                        0 <= radar_y < self.radar_size):
                        # Draw NPC dot (blue for NPCs)
                        pygame.draw.circle(radar_surface, (0, 191, 255), 
                                         (radar_x, radar_y), 3)  # Light blue dot for NPCs
            except AttributeError:
                pass  # Skip if game doesn't have NPCs
            
            # Add semi-transparent background
            background = pygame.Surface((self.radar_size + 8, self.radar_size + 8))
            background.fill((40, 40, 40))  # Dark gray
            background.set_alpha(200)  # Semi-transparent
            screen.blit(background, (self.radar_position[0] - 4, self.radar_position[1] - 4))
            
            # Add radar to main screen
            screen.blit(radar_surface, self.radar_position)
            
            # Draw radar legend
            legend_y = self.radar_position[1] + self.radar_size + 5
            legend_x = self.radar_position[0]
            legend_font = pygame.font.Font(None, 20)
            
            # Player legend
            pygame.draw.circle(screen, (0, 255, 0), (legend_x + 5, legend_y), 3)
            player_text = legend_font.render("Player", True, (255, 255, 255))
            screen.blit(player_text, (legend_x + 15, legend_y - 5))
            
            # Enemy legend
            pygame.draw.circle(screen, (255, 0, 0), (legend_x + 65, legend_y), 3)
            enemy_text = legend_font.render("Enemy", True, (255, 255, 255))
            screen.blit(enemy_text, (legend_x + 75, legend_y - 5))
            
            # NPC legend
            pygame.draw.circle(screen, (0, 191, 255), (legend_x + 125, legend_y), 3)
            npc_text = legend_font.render("NPC", True, (255, 255, 255))
            screen.blit(npc_text, (legend_x + 135, legend_y - 5))
        
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

    def toggle_radar(self):
        self.show_radar = not self.show_radar 