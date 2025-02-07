# render_factory.py
from abc import ABC, abstractmethod
from typing import Dict
from entity import Entity
import pygame # type: ignore

class textureFactory:

  def __init__(self):
    self.renderStrategies: Dict[str, RenderStrategy] = {}

  def renderEntity(self, entity: Entity, screen):
    strategy = self.renderStrategies.get(entity.entityType)
    if strategy:
      strategy.render(entity, screen)

class RenderStrategy(ABC):
  @abstractmethod
  def render(self, entity: Entity, screen):
    pass