def load_sounds(self):
    try:
        self.sounds = {
            'sword_swing': pygame.mixer.Sound(SWORD_SWING_SOUND),
            'hit': pygame.mixer.Sound(HIT_SOUND),
            'player_hurt': pygame.mixer.Sound(PLAYER_HURT_SOUND),
            'item_pickup': pygame.mixer.Sound(ITEM_PICKUP_SOUND)
        }
    except pygame.error:
        print("Error loading sounds") 