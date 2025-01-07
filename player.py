# player.py
import pygame # type: ignore
from sprites import player_images

class Player:
  def __init__(self, start_pos):
    self.player_pos = start_pos
    self.player_speed = 10
    self.direction = None
    self.last_direction = "R"
    self.counter = 0
    self.color = 'red'

  def animate(self):
    if self.counter < 19:
      self.counter += 1
    else:
      self.counter = 0

  def draw(self, screen):
    if self.last_direction == "R":
      screen.blit(player_images[self.counter // 5], self.player_pos)
    elif self.last_direction == "L":
      screen.blit(pygame.transform.flip(player_images[self.counter // 5], True, False), self.player_pos)
    elif self.last_direction == "U":
      screen.blit(pygame.transform.rotate(player_images[self.counter // 5], 90), self.player_pos)
    elif self.last_direction == "D":
      screen.blit(pygame.transform.rotate(player_images[self.counter // 5], 270), self.player_pos)

  def displayHitbox(self, screen):
    pygame.draw.rect(screen, self.color, (self.player_pos[0], self.player_pos[1], 50, 50))

  def move(self):
    if self.direction == "R": 
      self.player_pos[0] += self.player_speed
      self.last_direction = self.direction
    elif self.direction == "L": 
      self.player_pos[0] -= self.player_speed
      self.last_direction = self.direction
    elif self.direction == "U": 
      self.player_pos[1] -= self.player_speed
      self.last_direction = self.direction
    elif self.direction == "D": 
      self.player_pos[1] += self.player_speed
      self.last_direction = self.direction

  def set_direction(self, direction):
    self.direction = direction

  def stop(self):
    self.direction = None

  def reset_position(self, start_pos):
    self.player_pos = start_pos