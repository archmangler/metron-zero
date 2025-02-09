import os

class SaveSystem:
    def __init__(self, game):
        self.game = game
        self.save_folder = os.path.join(BASE_DIR, 'saves')
        self.ensure_save_directory()

    def ensure_save_directory(self):
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder) 