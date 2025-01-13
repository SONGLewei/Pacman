# game.py
import os
import sys
import math
import pygame # type: ignore

from level1 import boards
from level import Level
from player import Player

class Game:
  def __init__(self):
    self.WIDTH = 900
    self.HEIGHT = 1000
    self.fps = 60
    self.score = 0
    self.lives = 3
    self.isRunning = True
    self.currentLevel = Level()
    pygame.init()
    pygame.display.set_caption("Pac-Man")
    self.font = pygame.font.Font('./assets/fonts/Ubuntu.ttf', 20)
    self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
    self.timer = pygame.time.Clock()

  def startGame(self):
    self.currentLevel.loadLevel()
    self.run()

  def update(self):
    self.currentLevel.update()

  def render(self):
    self.screen.fill('black')
    self.currentLevel.render(self.screen)
    pygame.display.flip()

  def endGame(self):
    self.isRunning = False
    pygame.quit()

  def run(self):
    while self.isRunning:
      self.timer.tick(self.fps)
      self.update()
      self.render()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.endGame()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RIGHT: self.currentLevel.player.set_direction("R")
          elif event.key == pygame.K_LEFT: self.currentLevel.player.set_direction("L")
          elif event.key == pygame.K_UP: self.currentLevel.player.set_direction("U")
          elif event.key == pygame.K_DOWN: self.currentLevel.player.set_direction("D")
        if event.type == pygame.KEYUP:
          if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
            self.currentLevel.player.stop()
          elif event.key == pygame.K_SPACE:
            self.currentLevel.player.reset_position([450, 663])

if __name__ == "__main__":
  game = Game()
  game.startGame()