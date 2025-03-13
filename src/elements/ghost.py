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
    self.state = "dead"
    self.image = self.getImage()

    self.direction = None
    self.last_direction = None

    # Spawn tile is where the ghost will go when it is dead
    self.spawn_tile = [x * self.tileWidth, y * self.tileHeight]
    self.target_tile = [0, 0]
    self.respawn_timer = 3 * 60
    
    # Right, Left, Up, Down
    self.movable = [True, True, True, True]

  def setSpeed(self, speed):
    self.speed = speed

  def setTargetTile(self, x, y):
    self.target_tile = [x, y]

  def setDirection(self, direction):
    self.direction = direction

  # Chasing behaviour
  def isChasing(self) -> bool:
    return self.state == "chase"
  
  def setChasing(self) -> None:
    self.state = "chase"
    self.image = self.getImage()

  # Frightened behaviour
  def isFrightened(self) -> bool:
    return self.state == "frightened"
  
  def setFrightened(self) -> None:
    # If the ghost is dead, it won't be frightened
    if not self.isDead():
      self.last_direction = None
      self.setSpeed(0.5 * self.speed)
      self.state = "frightened"
      self.image = self.getImage()
  
  # Dead behaviour
  def isDead(self) -> bool:
    return self.state == "dead"
  
  def setDead(self) -> None:
    self.state = "dead"
    self.image = self.getImage()

  def respawn(self) -> None:
    if self.isOnSpawnTile():
      # print("Respawning")
      self.respawn_timer -= 1
      if self.respawn_timer <= 0:
        self.setSpawning()
        self.setSpeed(2)
        self.respawn_timer = 3 * 60
    else:
      print("This should not happen. Panic.")
      print(f"{self.x}, {self.y}, {self.spawn_tile[0]}, {self.spawn_tile[1]}")
      sys.exit()

  def isSpawning(self) -> bool:
    return self.state == "spawning"
  
  def setSpawning(self) -> None:
    self.state = "spawning"
    self.image = self.getImage()

  # Positioning
  def isOnTile(self) -> bool:
    return self.x % 30 == 0 and self.y % 30 == 0
  
  def isInSpawnBox(self) -> bool:
    return 11 <= self.x // 30 <= 18 and 11 <= self.y // 30 <= 17
  
  def isOnSpawnTile(self) -> bool:
    return self.x == self.spawn_tile[0] and self.y == self.spawn_tile[1]

  # Movement methods

  def move(self, player):
    # Only choose a target when exactly on a tile
    if self.isOnTile():
      
      if self.isDead():
        # Move towards the spawn box
        if (self.x // 30 == 14 and self.y // 30) == 12 or (self.x // 30 == 15 and self.y // 30 == 12):
          self.enterSpawnBox()
        elif self.isOnSpawnTile():
          self.respawn()
        else:
          self.deadMove()
        if self.isInSpawnBox():
          pass
            
          # Move towards spawn tile
          # if not self.isOnSpawnTile():
          #   self.deadMove()

      if self.isSpawning():
        if self.x // 30 == 14 and self.y // 30 == 12:
          self.setChasing()
        else:
          self.last_direction = None
          self.leaveSpawnBox()

      if not self.isSpawning() and not self.isDead():
       
      # else:
      #   # Choose target depending on the state of the ghost
        if self.isChasing():
          self.chaseMove(player)
      #   elif self.isScattering():
      #     self.scatterMove()
      #   elif self.isFrightened():
      #     self.frightenedMove()

    else:
      self.moveTowardsTarget()

    # Tunnel teleportation
    if self.x >= 900:
      self.x = 0
    elif self.x < 0:
      self.x = 900

    self.updateHitbox()

  def enterSpawnBox(self):
    tile_below_gate = (14, 14)
    self.setTargetTile(tile_below_gate[0] * 30, tile_below_gate[1] * 30)
    self.chooseDirection()
    self.last_direction = self.direction
    self.moveTowardsTarget()


  def leaveSpawnBox(self):
    tile_above_gate = (14, 12)
    self.setTargetTile(tile_above_gate[0] * 30, tile_above_gate[1] * 30)
    # if self.ghost_type == "red":
    #   print(f"Red ghost: {self.x}, {self.y}, {self.target_tile[0]}, {self.target_tile[1]}")
    self.chooseDirection()
    self.moveTowardsTarget()

  def moveTowardsTarget(self):
    if self.direction == "R" and self.canMove("R"):
      self.x += self.speed
    elif self.direction == "L" and self.canMove("L"):
      self.x -= self.speed
    elif self.direction == "U" and self.canMove("U"):
      self.y -= self.speed
    elif self.direction == "D" and self.canMove("D"):
      self.y += self.speed
  
  def chaseMove(self, player):
    if self.ghost_type == "red":
      self.blinkyChase(player)
    elif self.ghost_type == "pink":
      self.pinkyChase(player)
    elif self.ghost_type == "blue":
      self.inkyChase(player)
    elif self.ghost_type == "orange":
      self.clydeChase(player)
    self.chooseDirection()
    self.last_direction = self.direction
    self.moveTowardsTarget()
    
  def deadMove(self):
    self.setTargetTile(self.spawn_tile[0], self.spawn_tile[1])
    self.chooseDirection()
    self.last_direction = self.direction
    self.moveTowardsTarget()

  def movePosition(self, x, y):
    self.x = x * 30
    self.y = y * 30
    self.updateHitbox()

  # Blinky targets the player's current position
  def blinkyChase(self, player):
    self.setTargetTile(player.x, player.y)

  # Pinky targets the tile 4 tiles in front of the player
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

    self.setTargetTile(self.target_tile[0], self.target_tile[1])
    
  # Inky targets the tile 4 tiles in the back of the player
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

    self.setTargetTile(self.target_tile[0], self.target_tile[1])

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

    self.setTargetTile(self.target_tile[0], self.target_tile[1])

  def chooseDirection(self):
    # Calculate the distance to the target tile for all 4 possible directions
    up = round(self.calculateDistance(self.x, self.y - 30, self.target_tile[0], self.target_tile[1]))
    left = round(self.calculateDistance(self.x - 30, self.y, self.target_tile[0], self.target_tile[1]))
    down = round(self.calculateDistance(self.x, self.y + 30, self.target_tile[0], self.target_tile[1]))
    right = round(self.calculateDistance(self.x + 30, self.y, self.target_tile[0], self.target_tile[1]))

    directions = [
      ("U", up),
      ("L", left),
      ("D", down),
      ("R", right)
    ]

    # Sort first by distance. If distances are equal, sort by the order of Up, Left, Down, Right
    directions = sorted(directions, key=lambda x: (x[1], ["U", "L", "D", "R"].index(x[0])))

    # Try to move in the direction with the minimum distance
    for direction, distance in directions:
      if self.canMove(direction) and not self.isBacktracking(direction):
        self.setDirection(direction)
        break


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

  def canMove(self, direction: str) -> bool:
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
  
  # If the ghost is colliding with a wall in the next frame, make that position unmovable
  def handleCollision(self, entity) -> None:
    if self.hitbox.move(self.speed, 0).colliderect(entity.hitbox):
      self.setMovable("R", False)
    if self.hitbox.move(-self.speed, 0).colliderect(entity.hitbox):
      self.setMovable("L", False)
    if self.hitbox.move(0, -self.speed).colliderect(entity.hitbox):
      self.setMovable("U", False)
    if self.hitbox.move(0, self.speed).colliderect(entity.hitbox):
      self.setMovable("D", False)

  # Check if the ghost will collide with an entity in the next frame
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
  
  # Checks if the ghost is currently colliding with an entity
  def collide(self, entity) -> bool:
    return self.hitbox.colliderect(entity.hitbox)

  def getImage(self):
    if self.isFrightened():
      return spooked_img
    elif self.isDead():
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
    # Draw hitbox
    pygame.draw.rect(screen, 'red', self.hitbox, 1)
    pass