import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.randomAI import RandomAI
from controller.game import Game

if __name__ == "__main__":
  game = Game()
  #ai_agent = RandomAI()
  #game.enable_ai(ai_agent)
  game.startGame()