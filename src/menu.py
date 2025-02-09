import pygame
from config import *
import sys

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

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
        
    def draw(self, screen):
        screen.fill(self.background_color)
        
        if self.game_over:
            self.draw_game_over(screen)
        else:
            self.draw_main_menu(screen)
            
        pygame.display.flip()
    
    def draw_main_menu(self, screen):
        # Draw title
        title = self.font.render('Metron-Zero', True, self.text_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.text_color
            text = self.font.render(option, True, color)
            
            # Center the text
            x = SCREEN_WIDTH // 2
            y = SCREEN_HEIGHT // 2 + (i - len(self.options) // 2) * (self.button_height + self.button_padding)
            
            # Draw button background
            button_rect = pygame.Rect(
                x - self.button_width // 2,
                y - self.button_height // 2,
                self.button_width,
                self.button_height
            )
            pygame.draw.rect(screen, color, button_rect, 2)
            
            # Draw text
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
    
    def draw_game_over(self, screen):
        # Draw game over text
        game_over_text = self.font.render('Game Over', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(game_over_text, text_rect)
        
        # Draw score or stats if available
        if hasattr(self.game, 'score'):
            score_text = self.small_font.render(f'Score: {self.game.score}', True, self.text_color)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(score_text, score_rect)
        
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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            self.handle_input(event)
        return True

    def draw(self, surface):
        surface.fill(BLACK)
        
        # Draw title
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("2D RPG Game", True, WHITE)
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4)
        )
        surface.blit(title_text, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface) 
