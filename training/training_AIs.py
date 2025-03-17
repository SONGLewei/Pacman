import math
from src.controller.game import Game
from elements.dot import Dot
from elements.bigDot import BigDot
from training.pacmanAI import PacmanOfReseauNeuron
"""
    The father is Game, we will use this to train the AI, UI will not be active.
"""
class TrainingGame(Game):
    def __init__(self, ai_agent=None, max_steps=100000):
        super().__init__()
        self.ai_agent = ai_agent
        self.max_steps = max_steps

    def startGame(self):
        self.resetGameState()
        return self.run()
    
    def run(self):
        self.oneGame()
    
    def endGame(self):
        self.isRunning = False

    def resetGameState(self):
        self.score = 0
        self.isRunning = True
        self.loadLevel()
        self.loadConfig()
        self.staticEntities.clear()
        self.movableEntities.clear()

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
        wall_up = 1 if (pacman_x, pacman_y - 1) in self.walls else 0
        wall_down = 1 if (pacman_x, pacman_y + 1) in self.walls else 0
        wall_left = 1 if (pacman_x - 1, pacman_y) in self.walls else 0
        wall_right = 1 if (pacman_x + 1, pacman_y) in self.walls else 0

        # Ate bigDot or not
        pacman_powered_up = 1 if self.player.powered_up else 0
        ghost_scared = 1 if any(g.scared for g in self.movableEntities) else 0

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
        step = 0
        self.ai_agent = PacmanOfReseauNeuron()

        while self.isRunning and step<self.max_steps:
            step+=1
            state = self.get_game_state()
            action = self.ai_agent.getDecision(state)

            self.player.setDirection(action)
            super().update()

            if not self.isRunning:
                break

        print(f"Game end the score：{self.score}")
            