import os
import sys
import math
import pygame # type: ignore
import json

from levels.level import level_1
from elements.entity import Entity
from elements.dot import Dot
from elements.bigDot import BigDot
from elements.wall import Wall
from elements.cornerWall import CornerWall
from elements.gate import Gate
from elements.player import Player
from elements.ghost import Ghost
from typing import List

class Game:
  def __init__(self,headless = False):
    self.WIDTH = 900
    self.HEIGHT = 1000
    self.fps = 60
    self.score = 0
    self.isRunning = True
    self.staticEntities: List[Entity] = []
    self.movableEntities: List[Entity] = []

    if not headless:
      pygame.display.init()
      pygame.font.init()
      pygame.display.set_caption("Pac-Man")
      self.font = pygame.font.Font('./assets/fonts/Ubuntu.ttf', 20)
      self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
      self.clock = pygame.time.Clock()
    else:
      self.font = None
      self.screen = None
      self.clock = None
    self.loadConfig()

  def loadConfig(self):
    with open('./src/config.json', 'r') as f:
      data = json.load(f)
      self.player = Player(data['player']['start_pos'])
      for ghost in data['ghosts']:
        ghost_type = ghost['type']
        ghost_pos = ghost['start_pos']
        self.movableEntities.append(Ghost(ghost_pos[0], ghost_pos[1], ghost_type))
        pass

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
        # Gate
        elif tile == 9:
          self.staticEntities.append(Gate(j, i, 1))

  def startGame(self):
    self.loadLevel()
    self.run()

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
    #pygame.quit()

  def run(self):
    while self.isRunning:
      self.update()
      self.render()
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.endGame()
        if event.type == pygame.KEYDOWN:
          self.handleKeypress(event)

      self.clock.tick(self.fps)

  def update(self):
    self.player.animate()
    self.player.resetMovable()
    self.player.tickPowerUp(self.movableEntities)

    for ghost in self.movableEntities:
      ghost.resetMovable()

    for e in self.staticEntities:
      if isinstance(e, (Wall, CornerWall)):
        # Prevent the player from going through walls
        if self.player.willCollide(e):
          self.player.handleCollision(e)
        # Prevent ghosts from going through walls
        for ghost in self.movableEntities:
          if ghost.willCollide(e):
            ghost.handleCollision(e)

      if isinstance(e, Gate):
        # Prevent the player from going through the gate
        if self.player.willCollide(e):
          self.player.handleCollision(e)
        for ghost in self.movableEntities:
          # Prevent alive ghosts from entering
          if not ghost.isDead() and not ghost.isSpawning():
            if ghost.willCollide(e):
              ghost.handleCollision(e)


      # Eating the dots
      if isinstance(e, Dot) and self.player.collide(e):
        self.score += 10
        self.staticEntities.remove(e)

      # Eating the bigDots
      if isinstance(e, BigDot):
        e.animate()
        if self.player.collide(e):
          self.score += 50
          self.staticEntities.remove(e)
          self.player.powerUp()
          for ghost in self.movableEntities:
            ghost.setFrightened()

    self.player.move()
    
    for ghost in self.movableEntities:
      ghost.move(self.player)
      if ghost.collide(self.player) and not ghost.isDead():
        if self.player.isEmpowered:
          self.score += 200 * (2 ** self.player.ghostsEaten)
          self.player.ghostsEaten += 1
          ghost.setDead()
        else:
          print("Score: ", self.score)
          self.endGame()
      pass

    # Check if all dots and big dots are collected
    if not any(isinstance(e, (Dot, BigDot)) for e in self.staticEntities):
      print("You won!")
      self.endGame()

  def handleKeypress(self, event):
    if event.key == pygame.K_RIGHT: self.player.setDirection("R")
    elif event.key == pygame.K_LEFT: self.player.setDirection("L")
    elif event.key == pygame.K_UP: self.player.setDirection("U")
    elif event.key == pygame.K_DOWN: self.player.setDirection("D")
    elif event.key == pygame.K_SPACE: 
      for ghost in self.movableEntities:
        ghost.movePosition(2, 2)