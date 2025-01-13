# dot.py
import pygame # type: ignore

class Dot:
  def __init__(self, x, y, size, color='white'):
    self.x = x
    self.y = y
    self.size = size
    self.color = color

  def draw(self, screen):
    pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)