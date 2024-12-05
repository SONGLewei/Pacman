import pygame # type: ignore

player_images = []

for i in range(1, 5):
  player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (40, 40)))