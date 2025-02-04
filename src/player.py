from entity import Entity

import pygame # type: ignore

player_images = []
for i in range(1, 5):
  player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (40, 40)))

class Player(Entity):

  def __init__(self, start_pos):
    super().__init__(start_pos[0], start_pos[1])
    self.speed = 1
    self.direction = None
    self.last_direction = "R"
    self.counter = 0
    self.color = 'red'
    self.movable = [True, True, True, True]

  def move(self):
    if self.direction == "R" and self.movable[0]:
      self.x += self.speed
      self.last_direction = self.direction
    elif self.direction == "L" and self.movable[1]:
      self.x -= self.speed
      self.last_direction = self.direction
    elif self.direction == "U" and self.movable[2]:
      self.y -= self.speed
      self.last_direction = self.direction
    elif self.direction == "D" and self.movable[3]:
      self.y += self.speed
      self.last_direction = self.direction

  def setMovable(self, direction: str, move: bool) -> None:
    if direction == "R":
      self.movable[0] = move
    elif direction == "L":
      self.movable[1] = move
    elif direction == "U":
      self.movable[2] = move
    elif direction == "D":
      self.movable[3] = move

  def collide(self, entity) -> bool:
    return self.hitbox.colliderect(entity.hitbox)

  def render(self, screen) -> None:
    pygame.draw.rect(screen, self.color, self.hitbox, 2)
    if self.last_direction == "R":
      screen.blit(player_images[self.counter // 15], [self.x - 5, self.y - 5])
    elif self.last_direction == "L":
      screen.blit(pygame.transform.flip(player_images[self.counter // 15], True, False), [self.x - 5, self.y - 5])
    elif self.last_direction == "U":
      screen.blit(pygame.transform.rotate(player_images[self.counter // 15], 90), [self.x - 5, self.y - 5])
    elif self.last_direction == "D":
      screen.blit(pygame.transform.rotate(player_images[self.counter // 15], 270), [self.x - 5, self.y - 5])
    # Render player based on direction and animation
    
    pass

  def animate(self):
    if self.counter < 59:
      self.counter += 1
    else:
      self.counter = 0

  def set_direction(self, direction):
    self.direction = direction

  

  def reset_position(self, start_pos):
    self.x, self.y = start_pos