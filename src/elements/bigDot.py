from elements.entity import Entity

import pygame # type: ignore

class BigDot(Entity):
  def __init__(self, x: int, y: int):
    super().__init__(x, y)
    self.color: str = "white"
    self.size: int = 8
    self.counter: int = 0
    self.flicker: bool = False

  def render(self, screen):
    if not self.flicker:
      pygame.draw.circle(screen, self.color, (self.x + 0.5 * self.tileWidth, self.y + 0.5 * self.tileHeight), self.size)

  def animate(self):
    if self.counter < 120:
        self.counter += 1
        if self.counter > 60:
            self.flicker = False
    else:
        self.counter = 0
        self.flicker = True