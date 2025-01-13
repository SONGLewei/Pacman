# entity.py
from abc import ABC, abstractmethod
from typing import List
import pygame # type: ignore

class Entity(ABC):
  def __init__(self, x: int, y: int, entityType: str):
    self.x = x
    self.y = y
    self.entityType = entityType
    self.tileHeight = 30
    self.tileWidth = 30

  @abstractmethod
  def render(self, screen):
    pass

class StaticEntity(Entity):
  def __init__(self, x: int, y: int, isCollidable: bool):
    super().__init__(x, y, "Static")
    self.isCollidable = isCollidable

class MovableEntity(Entity):
  def __init__(self, x: int, y: int, speed: float):
    super().__init__(x, y, "Movable")
    self.speed = speed

class Wall(StaticEntity):
  def __init__(self, x: int, y: int, rotation: int):
    super().__init__(x, y, True)
    self.rotation = rotation

  def render(self, screen):
    # Draw vertical line
    if self.rotation == 0:
      pygame.draw.line(screen, 'blue', (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight), (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + self.tileHeight), 3)
    # Draw horizontal line
    elif self.rotation == 1:
      pygame.draw.line(screen, 'blue', (self.x * 30, self.y * 30 + 0.5 * self.tileHeight), (self.x * 30 + 30, self.y * 30 + 0.5 * self.tileHeight), 3)

class CornerWall(StaticEntity):
  def __init__(self, x: int, y: int, rotation: int):
    super().__init__(x, y, True)
    self.rotation = rotation

  def render(self, screen):
    # Top Right Corner
    if self.rotation == 0:
      pygame.draw.line(screen, 'blue', (self.x * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), 3)
      pygame.draw.line(screen, 'blue', (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + self.tileHeight), 3)
    # Top Left Corner
    elif self.rotation == 1:
      pygame.draw.line(screen, 'blue', (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), (self.x * self.tileWidth + self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), 3)
      pygame.draw.line(screen, 'blue', (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + self.tileHeight), 3)
    # Bottom Left Corner
    elif self.rotation == 2:
      pygame.draw.line(screen, 'blue', (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight), (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), 3)
      pygame.draw.line(screen, 'blue', (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), (self.x * self.tileWidth + self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), 3)
    # Bottom Right Corner
    elif self.rotation == 3:
      pygame.draw.line(screen, 'blue', (self.x * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), 3)
      pygame.draw.line(screen, 'blue', (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight), (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), 3)
    else:
      pass
      

class Dot(StaticEntity):
  def __init__(self, x: int, y: int):
    super().__init__(x, y, False)

  def render(self, screen):
    pygame.draw.circle(screen, 'white', (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), 4)

class BigDot(StaticEntity):
  def __init__(self, x: int, y: int):
    super().__init__(x, y, False)

  def render(self, screen):
    pygame.draw.circle(screen, 'white', (self.x * self.tileWidth + 0.5 * self.tileWidth, self.y * self.tileHeight + 0.5 * self.tileHeight), 8)