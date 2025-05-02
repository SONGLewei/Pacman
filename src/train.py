import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from training.training_AIs import TrainingGame

if __name__ == "__main__":

    game = TrainingGame()
    population = game.productTheFirstGeneration(1000)

    num_generations = 20
    fitness_log = []
    for gen in range(num_generations):
        print(f"\nGeneration {gen+1}:")

        results = game.runTheGeneration(population)

        population = game.evolve_population(results)

        best_score = max(score for _, score, _ in results)
        avg_score = sum(score for _, score, _ in results) / len(results)

        fitness_log.append({
        "generation": gen + 1,
        "best": best_score,
        "avg": avg_score
        })

        print(f"Best AI Score in Generation {gen+1}: {best_score}")

    game.saveRes(results, output_file="final_results.txt")
    game.saveResJson(results, output_file="final_res_json.json")

    with open("fitness_log.json", "w", encoding="utf-8") as f:
        json.dump(fitness_log, f, indent=4)

    print("Evolution completed!")