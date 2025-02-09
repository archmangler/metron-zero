import pygame
from config import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ['Start Game', 'Quit']
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game.state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        self.game.setup_game()
                        self.game.state = 'playing'
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        self.game.state = 'menu'
                        return True
                else:  # Regular menu handling
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Start Game
                            self.game.state = 'playing'
                            self.game.setup_game()
                        elif self.selected_option == 1:  # Quit
                            return False
                    elif event.key == pygame.K_ESCAPE:
                        return False
        return True
    
    def draw(self, screen):
        screen.fill(BLACK)
        
        if self.game.state == 'menu':
            # Draw title
            title = self.font.render('Metron-Zero', True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            screen.blit(title, title_rect)
            
            # Draw menu options
            for i, option in enumerate(self.options):
                color = RED if i == self.selected_option else WHITE
                text = self.small_font.render(option, True, color)
                pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)
                text_rect = text.get_rect(center=pos)
                screen.blit(text, text_rect)
        
        elif self.game.state == 'game_over':
            # Draw game over screen
            game_over = self.font.render('Game Over', True, RED)
            game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(game_over, game_over_rect)
            
            # Draw score
            score_text = self.small_font.render(f'Final Score: {self.game.score}', True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(score_text, score_rect)
            
            # Draw restart instructions
            restart_text = self.small_font.render('Press SPACE to restart or ESC to quit', True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3))
            screen.blit(restart_text, restart_rect)
        
        elif self.game.state == 'victory':
            # Draw victory screen
            victory_text = self.font.render('Victory!', True, (0, 255, 0))  # Green color
            victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(victory_text, victory_rect)
            
            # Draw score
            score_text = self.small_font.render(f'Final Score: {self.game.score}', True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(score_text, score_rect)
            
            # Draw congratulations
            congrats_text = self.small_font.render('Congratulations! You defeated all enemies!', True, WHITE)
            congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(congrats_text, congrats_rect)
            
            # Draw restart instructions
            restart_text = self.small_font.render('Press SPACE to play again or ESC to quit', True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
