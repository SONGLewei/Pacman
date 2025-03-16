import pygame
from src.controller.game import Game
"""
    The father is Game, we will use this to train the AI, UI will not be active.
"""
class TrainingGame(Game):
    def __init__(self, ai_agent=None, max_steps=100000):

        super().__init__()

        self.ai_agent = ai_agent
        self.max_steps = max_steps


    def resetGameState(self):
        pass

    def run_once(self):
        """
        Without the UI run the game
        """
        steps = 0
        self.isRunning = True

        while self.isRunning and steps < self.max_steps:
            steps += 1
            # 让AI 决定走哪
            if self.ai_agent:
                action = self.ai_agent.decide_action(self)
                self.player.setDirection(action)

            # Method of father
            super().update()

            # win or lost
            if not self.isRunning:
                break

        victory = False
        if (not any(self._is_dot(e) for e in self.staticEntities)):
            victory = True
        
        return self.score, victory

    def _is_dot(self, entity):
        # 简化判断
        return entity.__class__.__name__ in ["Dot", "BigDot"]

    def render(self):
        # empty
        pass

    def handleKeypress(self, event):
        pass
