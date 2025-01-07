# wall.py
import pygame # type: ignore

class Wall:
  def __init__(self, start_pos, end_pos, color='blue', width=3):
    self.start_pos = start_pos
    self.end_pos = end_pos
    self.color = color
    self.width = width

  def draw(self, screen):
    pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, self.width)