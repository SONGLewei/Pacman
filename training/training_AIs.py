import math

import numpy as np
import json
import random
import time
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
        self.last_time = time.time()
    def productTheFirstGeneration(self,population_size):
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
            self.last_position = (self.player.x, self.player.y)

            step = 0
            while self.isRunning and step < self.max_steps:
                step+=1
                state = self.get_game_state()
                action = self.ai_agent.getDecision(state)
                self.player.setDirection(action)
                super().update()
                self.dontMove360()

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
    
    def dontMove360(self):
        """
        Check if the player is stuck in a loop.
        If the player is stuck in a loop, end the game.
        This is the situations of the bugs.
        """
        current_position = (self.player.x, self.player.y)
        if current_position == self.last_position:
            self.frames_stuck += 1
        else:
            self.frames_stuck = 0
            self.last_position = current_position

        if self.frames_stuck >= 1000:
            print(f"Player stuck for 1000 frames,End the game")
            print("Score: ", self.score)
            self.endGame()

    def evolve_population(self,results, mutation_rate=0.03,mutation_strength=0.1):
        """
        evolve the next population of AI:40 indi   20 parents 10  20enfants 25
            1. keep top 12.5% individu 5
            2. crossover top 50% individu, each pair change weight on 50%, 2 times of crossover
            3. choose 15 AIs in the new generation, each weight have 2% to mutation
            4. the new generation also has 40 individu

        Evolve next generation:
            1. Keep 2 elites (best 2).
            2. Use roulette wheel to pick parents, produce 2 children each time
            3. Fill up the next generation to match population_size
            4. Mutate all individuals
            5. Return next generation
        """
        # take score and steps
        population = [ai for ai, _, _ in results]
        scores = [score for _, score, _ in results]

        #get the population size
        population_size = len(results)

        sum_score = sum(scores)

        sorted_results = sorted(results, key=lambda x: x[1],reverse=True)
        elite1 = sorted_results[0][0]
        elite2 = sorted_results[1][0]

        next_generation =[elite1,elite2]

        def roulette_selection():
            pick = random.random() * sum_score
            cumulative = 0
            for(ai,sc,_) in results:
                cumulative+=sc
                if cumulative>pick:
                    return ai

        while len(next_generation) < population_size:
            p1 = roulette_selection()
            p2 = roulette_selection()

            if p1 == p2:
                p2 = roulette_selection()

            #child1, child2 = self.uniform_crossover(p1, p2)
            child1, child2 = self.single_point_crossover(p1, p2)
            next_generation.append(child1)
            if len(next_generation) < population_size:
                next_generation.append(child2)

        for i,individual in enumerate(next_generation):
            if i>=2:
                self.mutate(individual, mutation_rate, mutation_strength)

        return next_generation

    def uniform_crossover(self, parent1, parent2):
        child1_weights = []
        child2_weights = []
        for w1, w2 in zip(parent1.network_weights, parent2.network_weights):
            mask = np.random.rand(*w1.shape) < 0.5
            c1 = np.where(mask, w1, w2)
            c2 = np.where(mask, w2, w1)
            child1_weights.append(c1)
            child2_weights.append(c2)

        c1 = PacmanOfReseauNeuron()
        c2 = PacmanOfReseauNeuron()
        c1.network_weights = child1_weights
        c2.network_weights = child2_weights
        return c1, c2
    
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
    
    def single_point_crossover(self, parent1, parent2):
        """
        Single-Point Crossover。
        """
        def flatten_network(weights_list):
            flat_parts = []
            shapes = []
            for w in weights_list:
                shapes.append(w.shape)
                flat_parts.append(w.flatten())
            flat_array = np.concatenate(flat_parts)
            return flat_array, shapes

        def unflatten_network(flat_array, shapes):
            restored = []
            offset = 0
            for shape in shapes:
                size = np.prod(shape)
                w_flat = flat_array[offset: offset + size]
                w_reshaped = w_flat.reshape(shape)
                restored.append(w_reshaped)
                offset += size
            return restored

        parent1_flat, shapes = flatten_network(parent1.network_weights)
        parent2_flat, _      = flatten_network(parent2.network_weights)

        length = len(parent1_flat)

        crossover_point = random.randint(1, length - 1)

        child1_flat = np.concatenate([
            parent1_flat[:crossover_point],
            parent2_flat[crossover_point:]
        ])

        child2_flat = np.concatenate([
            parent2_flat[:crossover_point],
            parent1_flat[crossover_point:]
        ])

        child1_weights = unflatten_network(child1_flat, shapes)
        child2_weights = unflatten_network(child2_flat, shapes)

        c1 = PacmanOfReseauNeuron()
        c1.network_weights = child1_weights
        c2 = PacmanOfReseauNeuron()
        c2.network_weights = child2_weights

        return c1, c2


    def mutate(self,individual, mutation_rate=0.05, mutation_strength=0.15):
        """
        each weight has 5% to mutate
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

        nearest_small_dot_dist = min((math.hypot(dot.x - pacman_x, dot.y - pacman_y) for dot in small_dots), default=0)
        nearest_big_dot_dist = min((math.hypot(dot.x - pacman_x, dot.y - pacman_y) for dot in big_dots), default=0)

        # The nearest 2 ghosts
        ghosts = sorted(self.movableEntities, key=lambda g: math.hypot(g.x - pacman_x, g.y - pacman_y))
        nearest_ghost_dist = math.hypot(ghosts[0].x - pacman_x, ghosts[0].y - pacman_y)
        second_ghost_dist = math.hypot(ghosts[1].x - pacman_x, ghosts[1].y - pacman_y)
        third_ghost_dist = math.hypot(ghosts[2].x - pacman_x, ghosts[2].y - pacman_y)
        forth_ghost_dist = math.hypot(ghosts[3].x - pacman_x, ghosts[3].y - pacman_y)

        # What's the direction of the ghosts
        pacman_pos = (pacman_x, pacman_y)
        ghost_angles = []

        for ghost in ghosts[:4]:
            ghost_pos = (ghost.x, ghost.y)
            angle = self.angle_between_radians(pacman_pos, ghost_pos)
            ghost_angles.append(angle)

        # (0,2π)
        direction_1_ghost = ghost_angles[0]
        direction_2_ghost = ghost_angles[1]
        direction_3_ghost = ghost_angles[2]
        direction_4_ghost = ghost_angles[3]

        # Walls detection
        wall_up = 0 if self.player.movable[2] else 1  # up
        wall_down = 1 if not self.player.movable[3] else 0  # down
        wall_left = 1 if not self.player.movable[1] else 0  # left
        wall_right = 1 if not self.player.movable[0] else 0  # right

        # Ate bigDot or not
        pacman_powered_up = 1 if self.player.isEmpowered else 0
        ghost_scared = 1 if any(g.state == "frightened" for g in self.movableEntities) else 0

        now = time.time()
        frame_duration = now - self.last_time
        self.last_time = now

        frame_duration = max(frame_duration,1e-6)
        self.current_fps = 1.0 / frame_duration

        normalized_fps = self.current_fps/100.0

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
            self.score / 1000,
            direction_1_ghost,
            direction_2_ghost,
            direction_3_ghost,
            direction_4_ghost,
            normalized_fps,
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

    @staticmethod
    def angle_between_radians(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        angle = math.atan2(dy, dx)
        angle_0_to_2pi = angle % (2 * math.pi)
        return angle_0_to_2pi