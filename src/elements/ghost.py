from elements.entity import Entity

import pygame # type: ignore

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
    self.speed = 1
    self.state = "chase"
    self.image = self.getImage()

  def move(self, player):
    if self.state == "chase":
      self.chase(player)
    elif self.state == "scatter":
      self.scatter()
    elif self.state == "frightened":
      self.frightened()
    elif self.state == "dead":
      self.dead()

  def chase(self, player):
    pass

  def scatter(self):
    # Move to a corner of the screen
    if self.ghost_type == "red":
      self.targe(0, 0)
    elif self.ghost_type == "pink":
      self.target(900, 0)
    elif self.ghost_type == "blue":
      self.target(900, 900)
    elif self.ghost_type == "orange":
      self.target(0, 900)

  def frightened(self):
    pass

  def dead(self):
    self.target(450, 450)

  def target(self, target_x, target_y):
    # Implement pathfinding to move towards the target position 
    if self.x < target_x:
      self.x += self.speed
    elif self.x > target_x:
      self.x -= self.speed
    if self.y < target_y:
      self.y += self.speed
    elif self.y > target_y:
      self.y -= self.speed
    self.updateHitbox()
  
  def distanceTo(self, player):
    return ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5

  def getImage(self):
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
