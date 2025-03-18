import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from training.training_AIs import TrainingGame

if __name__ == "__main__":
    training_game = TrainingGame()
    final_score = training_game.startGame()