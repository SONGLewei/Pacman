import math

import numpy as np
import json
from elements.cornerWall import CornerWall
from elements.gate import Gate
from src.controller.game import Game
from elements.dot import Dot
from elements.bigDot import BigDot
from training.pacmanAI import PacmanOfReseauNeuron
from elements.wall import Wall
"""
    The father is Game, we will use this to train the AI, UI will not be active.
"""
class TrainingGame(Game):
    def __init__(self, ai_agent=None, max_steps=100000):
        super().__init__(headless=True)
        
        self.ai_agent = ai_agent
        self.max_steps = max_steps

    def productTheFirstGeneration(self,population_size = 40):
        """
        The first step of GA, product a population with size of 40 if not indicate the nb
        of the generation
        """
        pacAIS = [PacmanOfReseauNeuron() for _ in range(population_size)]
        return pacAIS

    def runTheGeneration(self,pacAIS):
        """
        This function will use the list pacAIS to get all the evaluate score of individus
        entree : list pacAIS conclude all the individus
        sortie : score and themselves of these individus
        """
        results = []
        for pacAI in pacAIS:
            self.resetGameState()
            self.ai_agent = pacAI

            step = 0
            while self.isRunning and step < self.max_steps:
                step+=1
                state = self.get_game_state()
                action = self.ai_agent.getDecision(state)
                self.player.setDirection(action)
                super().update()

                if not self.isRunning:
                    break

            results.append((pacAI,self.score,step))

            if self.score >=9500 :
                special_file = f"high_score_ai_{self.score}.txt"
                self.saveHighScoreAI(pacAI, self.score, step, special_file)
                print(f"High score AI found! Saved to {special_file}")
                #return results
            
        results.sort(key=lambda x: x[1],reverse=True)
        return results

    def evolve_population(self,results, retain_ratio=0.125, mutation_rate=0.03, num_offspring=15):
        """
        evolve the next population of AI:40 indi   20 parents 10  20enfants 25
            1. keep top 12.5% individu 5
            2. crossover top 50% individu, each pair change weight on 50%, 2 times of crossover
            3. choose 15 AIs in the new generation, each weight have 2% to mutation
            4. the new generation also has 40 individu
        """

        population = [ai for ai, _, _ in results]
        scores = [score for _, score, _ in results]

        sorted_population = [p for _, p in sorted(zip(scores, population), key=lambda x: x[0], reverse=True)]

        num_retained = max(1, int(len(population) * retain_ratio))
        next_generation = sorted_population[:num_retained]

        num_parents = len(population) // 2
        parents = sorted_population[:num_parents]

        offspring = []
        for _ in range(2):
            np.random.shuffle(parents)
            for i in range(0, len(parents) - 1, 2):
                p1, p2 = parents[i], parents[i+1]
                child = self.crossover(p1, p2)
                offspring.append(child)
                if len(offspring) >= 20:
                    break

        next_generation.extend(offspring)

        mutated_offspring = np.random.choice(next_generation, num_offspring, replace=False)
        for individual in mutated_offspring:
            self.mutate(individual, mutation_rate)

        next_generation.extend(mutated_offspring)

        return next_generation
    
    def crossover(self,parent1, parent2):
        """
        crossover dad and mom, choose one, eachone has 50% percent
        """
        child_weights = []
        alpha = np.random.uniform(0.5, 0.9)
        for w1, w2 in zip(parent1.network_weights, parent2.network_weights):
            """
            Here, I choosed to let EACH data have 50% proba to get into the new children.
            But this perhaps will     change the good baby     , so this is difficult to get the better

            mask = np.random.rand(*w1.shape) < crossover_ratio
            child_w = np.where(mask, w1, w2)
            child_weights.append(child_w)
            """
            child_w = alpha * w1 + (1-alpha)*w2
            child_weights.append(child_w)

        child = PacmanOfReseauNeuron()
        child.network_weights = child_weights
        return child


    def mutate(self,individual, mutation_rate=0.01, mutation_strength=0.1):
        """
        each weight has 2% to mutate
        """
        for i in range(len(individual.network_weights)):
            mutation_mask = np.random.rand(*individual.network_weights[i].shape) < mutation_rate
            mutation_values = np.random.normal(0, mutation_strength, individual.network_weights[i].shape)
            individual.network_weights[i] += mutation_values * mutation_mask

    def startGame(self):
        self.resetGameState()
        return self.oneGame()
    
    def endGame(self):
        self.isRunning = False

    def resetGameState(self):
        self.score = 0
        self.isRunning = True
        self.staticEntities.clear()
        self.movableEntities.clear()
        self.loadConfig()
        self.loadLevel()


    def get_game_state(self):
        """
        The state of objects of this frame, these are the inputs of AI
        """
        # The position of AI
        pacman_x, pacman_y = self.player.x,self.player.y

        # The dots
        small_dots = [e for e in self.staticEntities if isinstance(e,Dot)]
        big_dots = [e for e in self.staticEntities if isinstance(e,BigDot)]

        nearest_small_dot_dist = min((math.hypot(dot.x - pacman_x, dot.y - pacman_y - pacman_y) for dot in small_dots), default=0)
        nearest_big_dot_dist = min((math.hypot(dot.x - pacman_x, dot.y - pacman_y) for dot in big_dots), default=0)

        # The nearest 2 ghosts
        ghosts = sorted(self.movableEntities, key=lambda g: math.hypot(g.x - pacman_x, g.y - pacman_y))
        nearest_ghost_dist = math.hypot(ghosts[0].x - pacman_x, ghosts[0].y - pacman_y)
        second_ghost_dist = math.hypot(ghosts[1].x - pacman_x, ghosts[1].y - pacman_y)
        third_ghost_dist = math.hypot(ghosts[2].x - pacman_x, ghosts[1].y - pacman_y)
        forth_ghost_dist = math.hypot(ghosts[3].x - pacman_x, ghosts[1].y - pacman_y)

        # Walls detection
        wall_up = 0 if self.player.movable[2] else 1  # up
        wall_down = 1 if not self.player.movable[3] else 0  # down
        wall_left = 1 if not self.player.movable[1] else 0  # left
        wall_right = 1 if not self.player.movable[0] else 0  # right

        # Ate bigDot or not
        pacman_powered_up = 1 if self.player.isEmpowered else 0
        ghost_scared = 1 if any(g.state == "frightened" for g in self.movableEntities) else 0

        input_vector = [
            pacman_x / self.WIDTH,
            pacman_y / self.HEIGHT,
            nearest_small_dot_dist / 100.0,
            len(small_dots) / 100.0,
            len(big_dots) / 10,
            nearest_ghost_dist / self.WIDTH,
            second_ghost_dist / self.WIDTH,
            third_ghost_dist / self.WIDTH,
            forth_ghost_dist / self.WIDTH,
            nearest_big_dot_dist / self.WIDTH,
            ghost_scared,
            wall_up,
            wall_down,
            wall_left,
            wall_right,
            pacman_powered_up,
            self.score / 1000
        ]

        return input_vector
    
    def oneGame(self):
        """
        The test of the whole process:
            1.get a new baby PacmanAI
            2.let this baby play one time the game
            3.get the score of the baby(Can show every step of the movements)
        """
        step = 0
        self.ai_agent = PacmanOfReseauNeuron()

        while self.isRunning and step<self.max_steps:
            step+=1
            state = self.get_game_state()
            action = self.ai_agent.getDecision(state)
            print(f"The direction is : {action}")
            self.player.setDirection(action)
            super().update()
            #print(f"Pacman position after move: ({self.player.x}, {self.player.y})")
            print(f"Pacman position after move: ({self.player.x}, {self.player.y}), Movable states: {self.player.movable}")

            if not self.isRunning:
                break

        print(f"Game end the score: {self.score}")
        return self.score
    
    def saveRes(self,results,output_file = "results.txt"):
        """
        Just save the resultats
        """
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("AI Evaluation Results\n")
            f.write("=" * 30 + "\n")

            for i, (ai, score, steps) in enumerate(results):
                result_str = f"AI #{i+1}: Score = {score}, Steps = {steps}\n"
                print(result_str, end="")
                f.write(result_str)

            f.write("=" * 30 + "\n")
            f.write(f"Total AIs Evaluated: {len(results)}\n")

        print(f"Evaluation completed. Results saved in {output_file}")
    
    def saveResJson(self, results, output_file="results.json"):
        """
        Json, score, steps 
        """
        data = {
            "total_evaluated": len(results),
            "ai_results": []
        }

        for i, (ai, score, steps) in enumerate(results):
            ai_data = {
                "id": i + 1,
                "score": score,
                "steps": steps,
                "network_weights": [layer.tolist() for layer in ai.network_weights]
            }

            data["ai_results"].append(ai_data)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"Evaluation finished. Results saved in {output_file}")

    def saveHighScoreAI(self, ai, score, steps, output_file):
        """
        When score>9500 save it
        """
        data = {
            "score": score,
            "steps": steps,
            "network_weights": [layer.tolist() for layer in ai.network_weights]
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"High score AI saved in {output_file}")