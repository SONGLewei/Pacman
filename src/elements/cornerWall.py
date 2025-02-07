from elements.entity import Entity

import pygame # type: ignore

class CornerWall(Entity):
  def __init__(self, x: int, y: int, rotation: int):
    super().__init__(x, y)
    self.rotation = rotation

  def render(self, screen):
    # Top Right Corner
    if self.rotation == 0:
      pygame.draw.line(screen, 'blue', (self.x, self.y + 0.5 * self.tileHeight), (self.x + 0.5 * self.tileWidth, self.y + 0.5 * self.tileHeight), 3)
      pygame.draw.line(screen, 'blue', (self.x + 0.5 * self.tileWidth, self.y + 0.5 * self.tileHeight), (self.x + 0.5 * self.tileWidth, self.y + self.tileHeight), 3)
    # Top Left Corner
    elif self.rotation == 1:
      pygame.draw.line(screen, 'blue', (self.x + 0.5 * self.tileWidth, self.y + 0.5 * self.tileHeight), (self.x + self.tileWidth, self.y + 0.5 * self.tileHeight), 3)
      pygame.draw.line(screen, 'blue', (self.x + 0.5 * self.tileWidth, self.y  + 0.5 * self.tileHeight), (self.x + 0.5 * self.tileWidth, self.y + self.tileHeight), 3)
    # Bottom Left Corner
    elif self.rotation == 2:
      pygame.draw.line(screen, 'blue', (self.x + 0.5 * self.tileWidth, self.y), (self.x + 0.5 * self.tileWidth, self.y + 0.5 * self.tileHeight), 3)
      pygame.draw.line(screen, 'blue', (self.x + 0.5 * self.tileWidth, self.y + 0.5 * self.tileHeight), (self.x + self.tileWidth, self.y + 0.5 * self.tileHeight), 3)
    # Bottom Right Corner
    elif self.rotation == 3:
      pygame.draw.line(screen, 'blue', (self.x, self.y + 0.5 * self.tileHeight), (self.x + 0.5 * self.tileWidth, self.y + 0.5 * self.tileHeight), 3)
      pygame.draw.line(screen, 'blue', (self.x + 0.5 * self.tileWidth, self.y), (self.x + 0.5 * self.tileWidth, self.y + 0.5 * self.tileHeight), 3)
    # Draw hitbox
    # pygame.draw.rect(screen, 'yellow', self.hitbox, 1)