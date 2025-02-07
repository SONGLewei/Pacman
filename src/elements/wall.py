from entity import Entity

import pygame # type: ignore

class Wall(Entity):
  def __init__(self, x: int, y: int, rotation: int):
    super().__init__(x, y)
    self.rotation = rotation

  def render(self, screen):
    # Draw vertical line
    if self.rotation == 0:
      pygame.draw.line(screen, 'blue', (self.x + 0.5 * self.tileWidth, self.y), (self.x + 0.5 * self.tileWidth, self.y + self.tileHeight), 3)
    # Draw horizontal line
    elif self.rotation == 1:
      pygame.draw.line(screen, 'blue', (self.x, self.y + 0.5 * self.tileHeight), (self.x + 30, self.y + 0.5 * self.tileHeight), 3)
    # Draw hitbox
    # pygame.draw.rect(screen, 'yellow', self.hitbox, 1)