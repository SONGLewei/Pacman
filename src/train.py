import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from training.training_AIs import TrainingGame

if __name__ == "__main__":
    training_game = TrainingGame()
    #final_score = training_game.startGame()

    pacman_population = training_game.productTheFirstGeneration()

    results = training_game.runTheGeneration(pacman_population)

    #training_game.saveResJson(results, output_file="results.json")
    training_game.saveRes(results, output_file="results.txt")