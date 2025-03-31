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

        with open('./visual/AI2.json','r',encoding='utf-8') as f:
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
        pacman_x, pacman_y = self.player.x, self.player.y

        small_dots = [e for e in self.staticEntities if isinstance(e, Dot)]
        big_dots = [e for e in self.staticEntities if isinstance(e, BigDot)]

        nearest_small_dot_dist = min(
            (math.hypot(dot.x - pacman_x, dot.y - pacman_y) for dot in small_dots),
            default=0
        )
        nearest_big_dot_dist = min(
            (math.hypot(dot.x - pacman_x, dot.y - pacman_y) for dot in big_dots),
            default=0
        )

        ghosts_sorted = sorted(
            self.movableEntities, 
            key=lambda g: math.hypot(g.x - pacman_x, g.y - pacman_y)
        )

        distances = [
            math.hypot(ghosts_sorted[i].x - pacman_x, ghosts_sorted[i].y - pacman_y)
            for i in range(4)
        ]

        angles = []
        pacman_pos = (pacman_x, pacman_y)
        for i in range(4):
            ghost_pos = (ghosts_sorted[i].x, ghosts_sorted[i].y)
            angle = self.angle_between_radians(pacman_pos, ghost_pos)
            angles.append(angle)

        wall_up    = 1 if not self.player.movable[2] else 0
        wall_down  = 1 if not self.player.movable[3] else 0
        wall_left  = 1 if not self.player.movable[1] else 0
        wall_right = 1 if not self.player.movable[0] else 0

        pacman_powered = 1 if self.player.isEmpowered else 0
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
            len(big_dots) / 10.0,
            distances[0] / self.WIDTH,
            distances[1] / self.WIDTH,
            distances[2] / self.WIDTH,
            distances[3] / self.WIDTH,
            nearest_big_dot_dist / self.WIDTH,
            ghost_scared,
            wall_up,
            wall_down,
            wall_left,
            wall_right,
            pacman_powered,
            self.score / 1000,
            angles[0],
            angles[1],
            angles[2],
            angles[3],
            normalized_fps,
        ]

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