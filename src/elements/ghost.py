from elements.entity import Entity
from queue import PriorityQueue

import pygame # type: ignore
import sys

blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (40, 40))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (40, 40))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (40, 40))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (40, 40))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (40, 40))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (40, 40))

class Ghost(Entity):
  def __init__(self, x, y, ghost_type):
    super().__init__(x, y)
    self.ghost_type = ghost_type
    self.speed = 2
    self.state = "chase"
    self.image = self.getImage()
    self.direction = None
    self.last_direction = None
    self.spawn_tile = [x, y]
    self.target_tile = [0, 0]
    self.movable = [True, True, True, True]
    self.inSpawnBox = True
    self.dead_timer = 0

    #pour test
    self.last_position = (self.x, self.y)
    self.idle_frames = 0

  def setSpeed(self, speed):
    self.speed = speed

  def setState(self, state):
    self.state = state
    self.image = self.getImage()
    if state != "frightened":
      self.setSpeed(2)
    if state == "dead":
      self.dead_timer = 6 * 60
      self.x, self.y = self.spawn_tile[0] * 30, self.spawn_tile[1] * 30
      self.inSpawnBox = False
      self.target_tile = [14 * 30, 12 * 30]

  def getState(self):
    return self.state
  
  def isInSpawnBox(self):
    return self.inSpawnBox
  
  def isDead(self):
    return self.state == "dead"
  
  def frighten(self):
    if not self.isDead():
      #self.last_direction = None
      self.setSpeed(0.5 * self.speed)
      self.setState("frightened")

  def move(self, player):
    #print("This is ")
    # Ghost will only choose a new target if they are exactly on a tile
    if self.isDead():
      self.dead()
      return
    
    if (self.state!="dead"):
      self.dead_timer = 0
    
    if self.x % 30 == 0 and self.y % 30 == 0:

      # Define the tile above the gate
      tile_above_gate = (14, 12)  # Adjust these coordinates based on your level design

      # Check if the ghost is inside the spawn box
      if 11 <= self.x // 30 <= 18 and 13 <= self.y // 30 <= 17:
        # Only go out of the box if we aren't currently going back to the spawn tile
        if not self.isDead():
          self.target_tile[0] = tile_above_gate[0] * 30
          self.target_tile[1] = tile_above_gate[1] * 30
          self.target(self.target_tile[0], self.target_tile[1])
          self.inSpawnBox = True
        # Otherwise go to the spawn tile and once on it set the state to chase
        else:
          self.dead()
          #if self.x == self.spawn_tile[0] and self.y == self.spawn_tile[1]:
          if self.x // 30 == self.spawn_tile[0] and self.y // 30 == self.spawn_tile[1]:
            self.inSpawnBox = True
            self.setState("chase")
      else:
        self.inSpawnBox = False

        # Depending on the state of the ghost it will move differently
        # Each of those method will choose the direction of the ghost.
        if self.state == "chase":
          self.chase(player)
        elif self.state == "scatter":
          self.scatter()
        elif self.state == "frightened":
          self.frightened(player)
        #elif self.state == "dead":
          #self.dead()

      # Now that the ghost has chosen a direction, it will move in that direction
      if self.direction == "R" and self.movable[0]:
        self.x += self.speed
        self.last_direction = self.direction
      if self.direction == "L" and self.movable[1]:
        self.x -= self.speed
        self.last_direction = self.direction
      if self.direction == "U" and self.movable[2]:
        self.y -= self.speed
        self.last_direction = self.direction
      if self.direction == "D" and self.movable[3]:
        self.y += self.speed
        self.last_direction = self.direction

      # If we aren't entirely on a tile, we keep moving in the same direction
    else:
      if self.last_direction == "R" and self.movable[0]:
        self.x += self.speed
      if self.last_direction == "L" and self.movable[1]:
        self.x -= self.speed
      if self.last_direction == "U" and self.movable[2]:
        self.y -= self.speed
      if self.last_direction == "D" and self.movable[3]:
        self.y += self.speed

    # Wrap around the screen horizontally
    if self.x >= 900:
      self.x = 0
    elif self.x < 0:
      self.x = 900

    self.updateHitbox()

    if (self.x, self.y) == self.last_position:
      self.idle_frames += 1
    else:
      self.idle_frames = 0
      self.last_position = (self.x, self.y)

    if self.idle_frames >= 60:
      if self.inSpawnBox and self.state != "dead":
            if self.direction == "R":
                self.movable[0] = True
            elif self.direction == "L":
                self.movable[1] = True
            elif self.direction == "U":
                self.movable[2] = True
            elif self.direction == "D":
                self.movable[3] = True
      print(f"this is {self.ghost_type}, my state: {self.state}, my direction: {self.direction}, my movable: {self.movable}, my dead_timer: {self.dead_timer}, in spawnBox: {self.inSpawnBox}")
 

  def chase(self, player):
    if self.ghost_type == "red":
      self.blinkyChase(player)
    elif self.ghost_type == "pink":
      self.pinkyChase(player)
    elif self.ghost_type == "blue":
      self.inkyChase(player)
    elif self.ghost_type == "orange":
      self.clydeChase(player)
    pass

  # Blinky targets the player's current position
  # All ghosts move with the following rules
  # 1. The target tile is the current position of the player
  # 1. It will take the direction that minimizes the distance to the target tile
  # 2. If it can't move in that direction, it will take the next best direction
  # 3. If 2 directions are equally good, it will follow the order of Up, Left, Down, Right
  # 4. It cannot move in the opposite direction of the last direction it moved in
  def blinkyChase(self, player):
    self.target_tile[0] = player.x
    self.target_tile[1] = player.y

    self.target(self.target_tile[0], self.target_tile[1])

  # Pinky targets the tile 4 tiles in front of the player
  # It also follows the general rules of movement
  def pinkyChase(self, player):
    # Target tile is 4 tiles in front of the player
    if player.direction == "R":
      self.target_tile[0] = player.x + 120
      self.target_tile[1] = player.y
    elif player.direction == "L":
      self.target_tile[0] = player.x - 120
      self.target_tile[1] = player.y
    elif player.direction == "U":
      self.target_tile[0] = player.x
      self.target_tile[1] = player.y - 120
    elif player.direction == "D":
      self.target_tile[0] = player.x
      self.target_tile[1] = player.y + 120
    elif player.direction == None:
      if player.last_direction == "R":
        self.target_tile[0] = player.x + 120
        self.target_tile[1] = player.y
      elif player.last_direction == "L":
        self.target_tile[0] = player.x - 120
        self.target_tile[1] = player.y
      elif player.last_direction == "U":
        self.target_tile[0] = player.x
        self.target_tile[1] = player.y - 120
      elif player.last_direction == "D":
        self.target_tile[0] = player.x
        self.target_tile[1] = player.y + 120

    self.target(self.target_tile[0], self.target_tile[1])
    
  # Inky targets the tile 4 tiles in the back of the player
  # 1. 
  def inkyChase(self, player):
    # Target tile is 4 tiles in front of the player
    if player.direction == "R":
      self.target_tile[0] = player.x - 120
      self.target_tile[1] = player.y
    elif player.direction == "L":
      self.target_tile[0] = player.x + 120
      self.target_tile[1] = player.y
    elif player.direction == "U":
      self.target_tile[0] = player.x
      self.target_tile[1] = player.y + 120
    elif player.direction == "D":
      self.target_tile[0] = player.x
      self.target_tile[1] = player.y - 120
    elif player.direction == None:
      if player.last_direction == "R":
        self.target_tile[0] = player.x - 120
        self.target_tile[1] = player.y
      elif player.last_direction == "L":
        self.target_tile[0] = player.x + 120
        self.target_tile[1] = player.y
      elif player.last_direction == "U":
        self.target_tile[0] = player.x
        self.target_tile[1] = player.y + 120
      elif player.last_direction == "D":
        self.target_tile[0] = player.x
        self.target_tile[1] = player.y - 120

    self.target(self.target_tile[0], self.target_tile[1])

  # Clyde targets the player if the distance between the player and Clyde is greater than 8 tiles
  # Otherwise, Clyde targets the bottom right corner
  def clydeChase(self, player):
    distance = self.calculateDistance(self.x, self.y, player.x, player.y)

    if distance > 240:
      self.target_tile[0] = player.x
      self.target_tile[1] = player.y
    else:
      self.target_tile[0] = 870
      self.target_tile[1] = 870

    self.target(self.target_tile[0], self.target_tile[1])

  def target(self, x, y):
    # Calculate the distance to the target tile for all 4 possible directions
    up = round(self.calculateDistance(self.x, self.y - 30, x, y))
    left = round(self.calculateDistance(self.x - 30, self.y, x, y))
    down = round(self.calculateDistance(self.x, self.y + 30, x, y))
    right = round(self.calculateDistance(self.x + 30, self.y, x, y))

    directions = [
      (up, "U"),
      (left, "L"),
      (down, "D"),
      (right, "R")
    ]

    # Sort first by distance. If distances are equal, sort by the order of Up, Left, Down, Right
    directions = sorted(directions, key=lambda x: (x[0], ["U", "L", "D", "R"].index(x[1])))

    # Try to move in the direction with the minimum distance
    for distance, directions in directions:
      if self.canMove(directions) and not self.isBacktracking(directions):
        self.setDirection(directions)
        break

  def scatter(self):
    # Blinky targets the top right corner
    if self.ghost_type == "red":
      self.target(870, 30)
    # Pinky targets the top left corner
    elif self.ghost_type == "pink":
      self.target(30, 30)
    # Inky targets the bottom right corner
    elif self.ghost_type == "blue":
      self.target(870, 870)
    elif self.ghost_type == "orange":
      self.target(0, 870)

  def frightened(self, player):
    x, y = player.x, player.y
    # Calculate the distance to the player in all 4 directions
    # Calculate the distance to the target tile for all 4 possible directions
    up = round(self.calculateDistance(self.x, self.y - 30, x, y))
    left = round(self.calculateDistance(self.x - 30, self.y, x, y))
    down = round(self.calculateDistance(self.x, self.y + 30, x, y))
    right = round(self.calculateDistance(self.x + 30, self.y, x, y))


    directions = [
      (up, "U"),
      (left, "L"),
      (down, "D"),
      (right, "R")
    ]
    
    # Reverse Sort by distance. If distances are equal, sort by the order of Up, Left, Down, Right
    directions = sorted(directions, key=lambda x: (x[0], ["R", "D", "L", "U"].index(x[1])), reverse=True)


    # Try to move in the direction with the maximum distance first
    for distance, direction in directions:
      #print(f"Direction: {direction}, canMove: {self.canMove(direction)}, isBacktracking: {self.isBacktracking(direction)}")
      if self.canMove(direction) :
        self.setDirection(direction)
        break

  def dead(self):
    if self.dead_timer > 0:
      self.dead_timer -= 1
    else:
      self.x = self.spawn_tile[0] * 30
      self.y = self.spawn_tile[1] * 30
      self.setState("chase")
      self.inSpawnBox = False
      self.speed = 2
      self.state = "chase"
      self.image = self.getImage()
      self.direction = "U"
      self.last_direction = "U"
      self.target_tile = [14 * 30, 12 * 30]
      self.movable = [True, True, True, True]
      self.dead_timer = 0

  def setDirection(self, direction):
    self.direction = direction

  def isBacktracking(self, direction):
    if direction == "R" and self.last_direction == "L":
      return True
    if direction == "L" and self.last_direction == "R":
      return True
    if direction == "U" and self.last_direction == "D":
      return True
    if direction == "D" and self.last_direction == "U":
      return True
    return False
  
  # Pythagorean theorem
  def calculateDistance(self, x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

  def canMove(self, direction):
    if direction == "R" and self.movable[0]:
      return True
    if direction == "L" and self.movable[1]:
      return True
    if direction == "U" and self.movable[2]:
      return True
    if direction == "D" and self.movable[3]:
      return True
    return False

  def setMovable(self, direction: str, move: bool) -> None:
    if direction == "R":
      self.movable[0] = move
    elif direction == "L":
      self.movable[1] = move
    elif direction == "U":
      self.movable[2] = move
    elif direction == "D":
      self.movable[3] = move

  def resetMovable(self) -> None:
    self.movable = [True, True, True, True]

  def updateHitbox(self) -> None:
    self.hitbox = pygame.Rect(self.x, self.y, 30, 30)
  
  def handleCollision(self, entity) -> None:
    if self.hitbox.move(self.speed, 0).colliderect(entity.hitbox):
      self.setMovable("R", False)
    if self.hitbox.move(-self.speed, 0).colliderect(entity.hitbox):
      self.setMovable("L", False)
    if self.hitbox.move(0, -self.speed).colliderect(entity.hitbox):
      self.setMovable("U", False)
    if self.hitbox.move(0, self.speed).colliderect(entity.hitbox):
      self.setMovable("D", False)

  def willCollide(self, entity) -> bool:
    if self.hitbox.move(self.speed, 0).colliderect(entity.hitbox):
      return True
    if self.hitbox.move(-self.speed, 0).colliderect(entity.hitbox):
      return True
    if self.hitbox.move(0, -self.speed).colliderect(entity.hitbox):
      return True
    if self.hitbox.move(0, self.speed).colliderect(entity.hitbox):
      return True
    return False
  
  def collide(self, entity) -> bool:
    return self.hitbox.colliderect(entity.hitbox)

  def getImage(self):
    if self.state == "frightened":
      return spooked_img
    elif self.state == "dead":
      return dead_img
    else:
      if self.ghost_type == "red":
        return blinky_img
      elif self.ghost_type == "pink":
        return pinky_img
      elif self.ghost_type == "blue":
        return inky_img
      elif self.ghost_type == "orange":
        return clyde_img

  def render(self, screen):
    screen.blit(self.image, (self.x - 5, self.y - 5))
    pass
