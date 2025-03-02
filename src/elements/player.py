from elements.entity import Entity

import pygame # type: ignore

player_images = []
for i in range(1, 5):
  player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (40, 40)))

class Player(Entity):

  def __init__(self, start_pos):
    super().__init__(start_pos[0], start_pos[1])
    self.speed = 2
    self.direction = None
    self.next_direction = None
    self.movable = [True, True, True, True]

    # Power Up Variables
    self.isEmpowered = False
    self.empowerCounter = 0
    self.ghostsEaten = 0

    self.counter = 0
    self.color = 'red'
    self.last_direction = "R"

  def powerUp(self):
    self.isEmpowered = True
    self.empowerCounter = 6 * 120
    self.ghostsEaten = 0

  def tickPowerUp(self, ghosts):
    if self.isEmpowered:
      self.empowerCounter -= 1
      if self.empowerCounter <= 0:
        self.isEmpowered = False
        for ghost in ghosts:
          ghost.setState("chase")

  def move(self):
    if self.next_direction != None:
      if self.canMove(self.next_direction):
        self.direction = self.next_direction
        self.next_direction = None

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

    # Wrap around the screen horizontally
    if self.x >= 900:
      self.x = 0
    elif self.x < 0:
      self.x = 900

    self.updateHitbox()

  def stop(self):
    self.direction = None

  def setDirection(self, direction):
    self.next_direction = direction

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

  def render(self, screen) -> None:
    if self.last_direction == "R":
      screen.blit(player_images[self.counter // 15], [self.x - 5, self.y - 5])
    elif self.last_direction == "L":
      screen.blit(pygame.transform.flip(player_images[self.counter // 15], True, False), [self.x - 5, self.y - 5])
    elif self.last_direction == "U":
      screen.blit(pygame.transform.rotate(player_images[self.counter // 15], 90), [self.x - 5, self.y - 5])
    elif self.last_direction == "D":
      screen.blit(pygame.transform.rotate(player_images[self.counter // 15], 270), [self.x - 5, self.y - 5])
    # Render player hitbox
    # pygame.draw.rect(screen, self.color, self.hitbox, 2)


  def animate(self):
    if self.counter < 29:
      self.counter += 1
    else:
      self.counter = 0