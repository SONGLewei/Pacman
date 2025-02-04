# game.py
import os
import sys
import math
import pygame # type: ignore

from level import level_1
from entity import Entity
from dot import Dot
from bigDot import BigDot
from wall import Wall
from cornerWall import CornerWall
from player import Player
from typing import List

class Game:
  def __init__(self):
    self.WIDTH = 900
    self.HEIGHT = 1000
    self.fps = 60
    self.score = 0
    self.lives = 3
    self.isRunning = True
    pygame.init()
    pygame.display.set_caption("Pac-Man")
    self.font = pygame.font.Font('./assets/fonts/Ubuntu.ttf', 20)
    self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
    # self.timer = pygame.time.Clock()
    self.staticEntities: List[Entity] = []
    self.movableEntities: List[Entity] = []
    self.player = Player([10, 12])

  def loadLevel(self, levelData: List[List[int]] = level_1):
    # Initialize entities based on levelData
    for i in range(len(levelData)):
      for j in range(len(levelData[i])):
        tile = levelData[i][j]
        if tile == 1:
          self.staticEntities.append(Dot(j, i))
        elif tile == 2:
          self.staticEntities.append(BigDot(j, i))
        # Vertical wall
        elif tile == 3:
          self.staticEntities.append(Wall(j, i, 0))
        # Horizontal wall
        elif tile == 4:
          self.staticEntities.append(Wall(j, i, 1))
        # Top Right Corner
        elif tile == 5:
          self.staticEntities.append(CornerWall(j, i, 0))
        # Top Left Corner
        elif tile == 6:
          self.staticEntities.append(CornerWall(j, i, 1))
        # Bottom Left Corner
        elif tile == 7:
          self.staticEntities.append(CornerWall(j, i, 2))
        # Bottom Right Corner
        elif tile == 8:
          self.staticEntities.append(CornerWall(j, i, 3))

  def startGame(self):
    self.loadLevel()
    self.run()

  def update(self):
    self.player.animate()

    for e in self.staticEntities:
      # If the type is Wall or CornerWall
      if(isinstance(e, Wall) or isinstance(e, CornerWall)):
        if self.player.collide(e):
          self.player.setMovable()

    self.player.move()

  def render(self):
    self.screen.fill('black')
    for entity in self.staticEntities:
      entity.render(self.screen)
    for entity in self.movableEntities:
      entity.render(self.screen)
    self.player.render(self.screen)
    pygame.display.flip()

  def endGame(self):
    self.isRunning = False
    pygame.quit()

  def run(self):
    while self.isRunning:
      self.update()
      self.render()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.endGame()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RIGHT: self.player.set_direction("R")
          elif event.key == pygame.K_LEFT: self.player.set_direction("L")
          elif event.key == pygame.K_UP: self.player.set_direction("U")
          elif event.key == pygame.K_DOWN: self.player.set_direction("D")
        if event.type == pygame.KEYUP:
          if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
            self.player.stop()