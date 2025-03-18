import math
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
            