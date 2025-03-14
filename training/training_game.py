from src.controller.game import Game

class TrainingGame(Game):
    def __init__(self, ai_agent=None, max_steps=2000):
        super().__init__()
        self.ai_agent = ai_agent
        self.max_steps = max_steps

    def resetGameState(self):
        pass

    def run_once(self):
        steps = 0
        self.isRunning = True

        while self.isRunning and steps < self.max_steps:
            steps += 1
            if self.ai_agent:
                action = self.ai_agent.decide_action(self)
                self.player.setDirection(action)

            super().update()

            if not self.isRunning:
                break

        victory = False
        if (not any(self._is_dot(e) for e in self.staticEntities)):
            victory = True
        
        return self.score, victory

    def _is_dot(self, entity):
        return entity.__class__.__name__ in ["Dot", "BigDot"]

    def render(self):
        pass

    def handleKeypress(self, event):
        pass
