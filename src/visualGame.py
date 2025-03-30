import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from visual.showAI import VisualAIPlayerGame

if __name__ == "__main__":
    game = VisualAIPlayerGame(headless=False)
    game.startGame()