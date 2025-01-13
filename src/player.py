from entity import MovableEntity

import pygame # type: ignore

player_images = []
for i in range(1, 5):
  player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (40, 40)))

class Player(MovableEntity):
  def __init__(self, start_pos):
    super().__init__(start_pos[0], start_pos[1], 10)
    self.direction = None
    self.last_direction = "R"
    self.counter = 0
    self.color = 'red'

  def move(self):
    if self.direction == "R":
      self.x += self.speed
      self.last_direction = self.direction
    elif self.direction == "L":
      self.x -= self.speed
      self.last_direction = self.direction
    elif self.direction == "U":
      self.y -= self.speed
      self.last_direction = self.direction
    elif self.direction == "D":
      self.y += self.speed
      self.last_direction = self.direction

  def render(self, screen):
    if self.last_direction == "R":
      screen.blit(player_images[self.counter // 5], [self.x, self.y])
    elif self.last_direction == "L":
      screen.blit(pygame.transform.flip(player_images[self.counter // 5], True, False), [self.x, self.y])
    elif self.last_direction == "U":
      screen.blit(pygame.transform.rotate(player_images[self.counter // 5], 90), [self.x, self.y])
    elif self.last_direction == "D":
      screen.blit(pygame.transform.rotate(player_images[self.counter // 5], 270), [self.x, self.y])
    # Render player based on direction and animation
    pass

  def animate(self):
    if self.counter < 19:
      self.counter += 1
    else:
      self.counter = 0

  def set_direction(self, direction):
    self.direction = direction

  def stop(self):
    self.direction = None

  def reset_position(self, start_pos):
    self.x, self.y = start_pos