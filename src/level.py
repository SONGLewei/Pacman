# level.py
from typing import List
from entity import StaticEntity, MovableEntity, Dot, BigDot, Wall, CornerWall
from player import Player
from level1 import boards

class Level:
  def __init__(self):
    self.staticEntities: List[StaticEntity] = []
    self.movableEntities: List[MovableEntity] = []
    self.player = Player([450, 663])

  def loadLevel(self, levelData: List[List[int]] = boards):
    # Initialize entities based on levelData
    for i in range(len(levelData)):
      for j in range(len(levelData[i])):
        tile = levelData[i][j]
        if tile == 1:
          self.staticEntities.append(Dot(j, i))
        elif tile == 2:
          self.staticEntities.append(BigDot(j, i))
        # Vertical wall
        elif tile == 3:
          self.staticEntities.append(Wall(j, i, 0))
        # Horizontal wall
        elif tile == 4:
          self.staticEntities.append(Wall(j, i, 1))
        # Top Right Corner
        elif tile == 5:
          self.staticEntities.append(CornerWall(j, i, 0))
        # Top Left Corner
        elif tile == 6:
          self.staticEntities.append(CornerWall(j, i, 1))
        # Bottom Left Corner
        elif tile == 7:
          self.staticEntities.append(CornerWall(j, i, 2))
        # Bottom Right Corner
        elif tile == 8:
          self.staticEntities.append(CornerWall(j, i, 3))
        # Add other entities as needed

  def resetLevel(self):
    self.loadLevel()

  def update(self):
    self.player.animate()
    self.player.move()
    # Update other movable entities

  def render(self, screen):
    for entity in self.staticEntities:
      entity.render(screen)
    for entity in self.movableEntities:
      entity.render(screen)
    self.player.render(screen)