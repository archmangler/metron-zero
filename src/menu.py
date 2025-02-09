import pygame
import sys
from config import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ['Start Game', 'Options', 'Quit']
        self.game_over = False
        
        # Colors
        self.text_color = WHITE
        self.selected_color = GREEN
        self.background_color = BLACK
        
        # Button dimensions
        self.button_width = 200
        self.button_height = 50
        self.button_padding = 20
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            self.handle_input(event)
            
        return True
        
    def draw(self, screen):
        # Clear screen
        screen.fill(self.background_color)
        
        if self.game_over:
            self.draw_game_over(screen)
        else:
            self.draw_main_menu(screen)
        
        # Update display
        pygame.display.flip()
    
    def draw_main_menu(self, screen):
        # Draw title
        title = self.font.render('Metron-Zero', True, self.text_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Calculate starting Y position for centering options vertically
        total_height = len(self.options) * (self.button_height + self.button_padding)
        start_y = (SCREEN_HEIGHT - total_height) // 2
        
        # Draw each option
        for i, option in enumerate(self.options):
            # Determine if this option is selected
            is_selected = i == self.selected_option
            color = self.selected_color if is_selected else self.text_color
            
            # Calculate position
            x = SCREEN_WIDTH // 2
            y = start_y + i * (self.button_height + self.button_padding)
            
            # Draw button background
            button_rect = pygame.Rect(
                x - self.button_width // 2,
                y,
                self.button_width,
                self.button_height
            )
            pygame.draw.rect(screen, color, button_rect, 2)
            
            # Draw text
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
    
    def draw_game_over(self, screen):
        # Draw game over text
        game_over_text = self.font.render('Game Over', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(game_over_text, text_rect)
        
        # Draw restart prompt
        restart_text = self.small_font.render('Press SPACE to restart', True, self.text_color)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        screen.blit(restart_text, restart_rect)
        
        # Draw quit prompt
        quit_text = self.small_font.render('Press ESC to quit', True, self.text_color)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3 + 40))
        screen.blit(quit_text, quit_rect)
    
    def handle_input(self, event):
        if self.game_over:
            self.handle_game_over_input(event)
        else:
            self.handle_menu_input(event)
    
    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.select_option()
    
    def handle_game_over_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.restart_game()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    def select_option(self):
        if self.options[self.selected_option] == 'Start Game':
            self.game.state = 'playing'
            self.game_over = False
        elif self.options[self.selected_option] == 'Options':
            # Implement options menu
            pass
        elif self.options[self.selected_option] == 'Quit':
            pygame.quit()
            sys.exit()
    
    def show_game_over(self):
        self.game_over = True
        self.game.state = 'menu'
    
    def restart_game(self):
        # Reset game state
        self.game.setup_game()
        self.game.state = 'playing'
        self.game_over = False
