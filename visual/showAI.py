import json
import math
import time
import numpy as np
import pygame

from src.controller.game import Game
from training.pacmanAI import PacmanOfReseauNeuron
from elements.dot import Dot
from elements.bigDot import BigDot
from elements.ghost import Ghost


class VisualAIPlayerGame(Game):
    def __init__(self, headless=False):
        super().__init__(headless = headless)
        self.last_time = time.time()

        #path = './visual/AI2.json' # It understands how to getaway from the pink ghost, but dont know to go right and up.
        path = './visual/3000.json'
        #path = './visual/AIstill.json'# Il est invincible
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
            weight_data = data["network_weights"]

        self.ai_agent = PacmanOfReseauNeuron()
        loaded_weight = []
        for layer2d in weight_data:
            arr = np.array(layer2d,dtype = float)
            loaded_weight.append(arr)

        self.ai_agent.network_weights = loaded_weight

    def run(self):
        self.loadLevel()

        while self.isRunning:
            state = self.get_game_state()
            action = self.ai_agent.getDecision(state)
            self.player.setDirection(action)

            super().update()

            if self.screen:
                super().render()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.endGame()
    
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
        ghost_dead = 1 if any(g.state == "dead" for g in self.movableEntities) else 0
        ghost_chase = 1 if any(g.state == "chase" for g in self.movableEntities) else 0
        ghost_spawning = 1 if any(g.state == "spawning" for g in self.movableEntities) else 0

        now = time.time()
        frame_duration = now - self.last_time
        self.last_time = now

        frame_duration = max(frame_duration,1e-6)
        self.current_fps = 1.0 / frame_duration

        normalized_fps = self.current_fps/100.0

        #mini 888888888888888888
        """
        input_vector = [
            pacman_x / self.WIDTH,
            pacman_y / self.HEIGHT,
            nearest_small_dot_dist / 100.0,
            nearest_ghost_dist / self.WIDTH,
            wall_up,
            wall_down,
            wall_left,
            wall_right
        ]
        """

        #milieu  1414141414141414
        
        input_vector = [
            pacman_x / self.WIDTH,
            pacman_y / self.HEIGHT,
            nearest_small_dot_dist / 100.0,
            len(small_dots) / 100.0,
            len(big_dots) / 10,
            nearest_ghost_dist / self.WIDTH,
            second_ghost_dist / self.WIDTH,
            ghost_scared,
            ghost_dead,
            ghost_chase,
            wall_up,
            wall_down,
            wall_left,
            wall_right
        ]
        

        # Le plus grand 252525252525
        """
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
            ghost_dead,
            ghost_spawning,
            ghost_chase,
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
        """
        return input_vector

    @staticmethod
    def angle_between_radians(p1, p2):

        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        angle = math.atan2(dy, dx)
        return angle % (2 * math.pi)

    def handleKeypress(self, event):
        if event.key == pygame.K_ESCAPE:
            self.endGame()
        return