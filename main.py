import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game import Game

if __name__ == '__main__':
    game = Game()
    game.run() 