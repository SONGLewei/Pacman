# game.py
import os
import sys
import math
import pygame # type: ignore

from board import boards

# Game Elements
from wall import Wall
from dot import Dot
from player import Player

class Game:
  def __init__(self):
    self.WIDTH = 900
    self.HEIGHT = 950
    self.fps = 60
    self.level = boards
    self.wall_color = 'blue'
    self.PI = math.pi
    self.player = Player([450, 663])
    self.counter = 0
    self.flicker = False
    pygame.init()
    pygame.display.set_caption("Pac-Man")
    self.font = pygame.font.Font('Ubuntu.ttf', 20)
    self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
    self.timer = pygame.time.Clock()
    self.running = True

  def drawBoard(self):
    num1 = (self.HEIGHT - 50) // 32
    num2 = (self.WIDTH // 30)
    for i in range(len(self.level)):
      for j in range(len(self.level[i])):

        # Position in the board
        x = j * num2 + num2 / 2
        y = i * num1 + num1 / 2

        if self.level[i][j] == 1:
          dot = Dot(x,y,4)
          dot.draw(self.screen)
        elif self.level[i][j] == 2 and not self.flicker:
          dot = Dot(x,y,8)
          dot.draw(self.screen)
        elif self.level[i][j] == 3:
          wall = Wall((j * num2 + 0.5 * num2, i * num1), (j * num2 + 0.5 * num2, i * num1 + num1), self.wall_color)
          wall.draw(self.screen)
        elif self.level[i][j] == 4:
          wall = Wall((j * num2, i * num1 + 0.5 * num1), (j * num2 + num2, i * num1 + 0.5 * num1), self.wall_color)
          wall.draw(self.screen)
        elif self.level[i][j] == 5:
          wall1 = Wall((j * num2, i * num1 + 0.5 * num1), (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), self.wall_color)
          wall2 = Wall((j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), (j * num2 + 0.5 * num2, i * num1 + num1), self.wall_color)
          wall1.draw(self.screen)
          wall2.draw(self.screen)
        elif self.level[i][j] == 6:
          wall1 = Wall((j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), (j * num2 + num2, i * num1 + 0.5 * num1), self.wall_color)
          wall2 = Wall((j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), (j * num2 + 0.5 * num2, i * num1 + num1), self.wall_color)
          wall1.draw(self.screen)
          wall2.draw(self.screen)
        elif self.level[i][j] == 7:
          wall1 = Wall((j * num2 + 0.5 * num2, i * num1), (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), self.wall_color)
          wall2 = Wall((j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), (j * num2 + num2, i * num1 + 0.5 * num1), self.wall_color)
          wall1.draw(self.screen)
          wall2.draw(self.screen)
        elif self.level[i][j] == 8:
          pygame.draw.line(self.screen, self.wall_color, (j * num2, i * num1 + 0.5 * num1), (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 3)
          pygame.draw.line(self.screen, self.wall_color, (j * num2 + 0.5 * num2, i * num1), (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 3)
        elif self.level[i][j] == 9:
          pygame.draw.line(self.screen, 'white', (j * num2, i * num1 + 0.5 * num1), (j * num2 + num2, i * num1 + 0.5 * num1), 3)

  def flickerDots(self):
    if self.counter > 10:
      self.flicker = True
    else:
      self.flicker = False

  def run(self):
    while self.running:
      self.timer.tick(self.fps)
      self.screen.fill('black')
      self.drawBoard()
      self.flickerDots()
      
      # Player
      self.player.draw(self.screen)
      # self.player.displayHitbox(self.screen)
      # self.player.animate()
          
      for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          self.running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RIGHT: self.player.set_direction("R")
          elif event.key == pygame.K_LEFT: self.player.set_direction("L")
          elif event.key == pygame.K_UP: self.player.set_direction("U")
          elif event.key == pygame.K_DOWN: self.player.set_direction("D")
        if event.type == pygame.KEYUP:
          if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]: 
            self.player.stop()
          elif event.key == pygame.K_SPACE: 
            self.player.reset_position([450, 663])

        pygame.display.flip()

    pygame.quit()