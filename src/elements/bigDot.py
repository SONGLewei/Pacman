from entity import Entity

import pygame # type: ignore

class BigDot(Entity):
  def __init__(self, x: int, y: int):
    super().__init__(x, y)
    self.color: str = "white"
    self.size: int = 8

  def render(self, screen):
    pygame.draw.circle(screen, self.color, (self.x + 0.5 * self.tileWidth, self.y + 0.5 * self.tileHeight), self.size)