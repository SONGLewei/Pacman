# render_factory.py
from typing import Dict
from entity import Entity

class RenderFactory:
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