import pygame
import os

class Game:
    def load_backgrounds(self):
        return {
            'sea': pygame.transform.scale(
                pygame.image.load(os.path.join(IMAGES_DIR, 'sea.png')).convert_alpha(),
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            ),
            'desert': pygame.transform.scale(
                pygame.image.load(os.path.join(IMAGES_DIR, 'desert.png')).convert_alpha(),
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            ),
            'hellscape': pygame.transform.scale(
                pygame.image.load(os.path.join(IMAGES_DIR, 'hellscape.png')).convert_alpha(),
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        } 