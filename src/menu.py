import pygame
from config import *

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
        self.buttons = []
        self.setup_menu()
    
    def setup_menu(self):
        # Main menu buttons
        start_btn = Button(
            SCREEN_WIDTH//2 - 100,
            SCREEN_HEIGHT//2 - 50,
            200, 50,
            "Start Game",
            (100, 100, 100),
            (150, 150, 150)
        )
        
        options_btn = Button(
            SCREEN_WIDTH//2 - 100,
            SCREEN_HEIGHT//2 + 20,
            200, 50,
            "Options",
            (100, 100, 100),
            (150, 150, 150)
        )
        
        quit_btn = Button(
            SCREEN_WIDTH//2 - 100,
            SCREEN_HEIGHT//2 + 90,
            200, 50,
            "Quit",
            (100, 100, 100),
            (150, 150, 150)
        )
        
        self.buttons = [start_btn, options_btn, quit_btn]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            for i, button in enumerate(self.buttons):
                if button.handle_event(event):
                    if i == 0:  # Start Game
                        self.game.state = 'playing'
                    elif i == 1:  # Options
                        self.game.state = 'options'
                    elif i == 2:  # Quit
                        return False
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