import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from training.training_AIs import TrainingGame

if __name__ == "__main__":
    """
    training_game = TrainingGame()
    #final_score = training_game.startGame()

    pacman_population = training_game.productTheFirstGeneration()

    results = training_game.runTheGeneration(pacman_population)

    #training_game.saveResJson(results, output_file="results.json")
    training_game.saveRes(results, output_file="results.txt")
    """

    game = TrainingGame()
    population = game.productTheFirstGeneration(80)

    num_generations = 10
    for gen in range(num_generations):
        print(f"\nGeneration {gen+1}:")

        results = game.runTheGeneration(population)

        population = game.evolve_population(results)

        best_score = max(score for _, score, _ in results)
        print(f"Best AI Score in Generation {gen+1}: {best_score}")

    game.saveRes(results, output_file="final_results.txt")
    game.saveResJson(results, output_file="final_res_json.json")
    print("Evolution completed!")