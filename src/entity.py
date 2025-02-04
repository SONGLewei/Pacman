# entity.py
from abc import ABC, abstractmethod
from typing import List
import pygame # type: ignore

# Abstract class
class Entity(ABC):
  def __init__(self, x: int, y: int):
    self.tileHeight: int = 30
    self.tileWidth: int = 30

    self.x: int = x * self.tileWidth
    self.y: int = y * self.tileHeight
    self.hitbox = pygame.rect.Rect(self.x, self.y, self.tileWidth, self.tileHeight)

  @abstractmethod
  def render(self, screen):
    # pygame.draw.rect(screen, 'white', self.hitbox)
    pass