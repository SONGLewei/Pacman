import os
import sys
import math
import pygame # type: ignore
from board import boards
from sprites import player_images

WIDTH = 900
HEIGHT = 950
fps = 60
level = boards
wall_color = 'blue'
PI = math.pi
# We are in a 2D game, so a list is enough to represent the position
player_pos = [450, 663]
direction = None
last_direction = "R"
counter = 0
flicker = False
directions = ["R", "L", "U", "D"]
player_speed = 2

def drawBoard():
  global flicker
  num1 = (HEIGHT - 50) // 32
  num2 = (WIDTH // 30)

  # Iterate through every rows
  for i in range(len(level)):
    # Iterate through every columns
    for j in range(len(level[i])):
      # Draw small dots
      if level[i][j] == 1:
        pygame.draw.circle(screen, 'white', (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 4)
      # Draw big dots
      elif level[i][j] == 2 and not flicker:
        pygame.draw.circle(screen, 'white', (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 8)
      # Draw vertical line
      elif level[i][j] == 3:
        pygame.draw.line(screen, wall_color, (j * num2 + 0.5 * num2, i * num1), (j * num2 + 0.5 * num2, i * num1 + num1), 3)
      # Draw horizontal line
      elif level[i][j] == 4:
        pygame.draw.line(screen, wall_color, (j * num2, i * num1 + 0.5 * num1), (j * num2 + num2, i * num1 + 0.5 * num1), 3)
      # Draw corner top right
      elif level[i][j] == 5:
        pygame.draw.line(screen, wall_color, (j * num2, i * num1 + 0.5 * num1), (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 3)
        pygame.draw.line(screen, wall_color, (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), (j * num2 + 0.5 * num2, i * num1 + num1), 3)
      # Draw corner top left
      elif level[i][j] == 6:
        pygame.draw.line(screen, wall_color, (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), (j * num2 + num2, i * num1 + 0.5 * num1), 3)
        pygame.draw.line(screen, wall_color, (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), (j * num2 + 0.5 * num2, i * num1 + num1), 3)
      # Draw corner bot left
      elif level[i][j] == 7:
        pygame.draw.line(screen, wall_color, (j * num2 + 0.5 * num2, i * num1), (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 3)
        pygame.draw.line(screen, wall_color, (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), (j * num2 + num2, i * num1 + 0.5 * num1), 3)
      # Draw corner bot right
      elif level[i][j] == 8:
        pygame.draw.line(screen, wall_color, (j * num2, i * num1 + 0.5 * num1), (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 3)
        pygame.draw.line(screen, wall_color, (j * num2 + 0.5 * num2, i * num1), (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 3)
      # Draw gate
      elif level[i][j] == 9:
        pygame.draw.line(screen, 'white', (j * num2, i * num1 + 0.5 * num1), (j * num2 + num2, i * num1 + 0.5 * num1), 3)

def animatePlayer():
  global counter
  if counter < 19:
    counter += 1
  else:
    counter = 0

def flickerDots():
  global counter
  global flicker
  if counter > 10:
    flicker = True
  else:
    flicker = False

def drawPlayer():
  if last_direction == "R":
    screen.blit(player_images[counter // 5], player_pos)
  elif last_direction == "L":
    screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), player_pos)
  elif last_direction == "U":
    screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), player_pos)
  elif last_direction == "D":
    screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), player_pos)

def movePlayer():
  global player_pos
  global direction, player_speed, last_direction
  if direction == "R": 
    player_pos[0] += player_speed
    last_direction = direction
  elif direction == "L": 
    player_pos[0] -= player_speed
    last_direction = direction
  elif direction == "U": 
    player_pos[1] -= player_speed
    last_direction = direction
  elif direction == "D": 
    player_pos[1] += player_speed
    last_direction = direction

if __name__ == "__main__":
  pygame.init()
  pygame.display.set_caption("Pac-Man")
  font = pygame.font.Font('Ubuntu.ttf', 20)
  screen = pygame.display.set_mode([WIDTH, HEIGHT])

  timer = pygame.time.Clock()
  running = True

  while running:
    timer.tick(fps)
    screen.fill('black')
    drawBoard()
    drawPlayer()
    animatePlayer()
    flickerDots()
    movePlayer()
    
    for event in pygame.event.get():
      # Handle Quit event
      if event.type == pygame.QUIT: running = False
      # Handle arrow keys
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT: direction = "R"
        elif event.key == pygame.K_LEFT: direction = "L"
        elif event.key == pygame.K_UP: direction = "U"
        elif event.key == pygame.K_DOWN: direction = "D"
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT: direction = None 
        elif event.key == pygame.K_LEFT: direction = None 
        elif event.key == pygame.K_UP: direction = None
        elif event.key == pygame.K_DOWN: direction = None
        elif event.key == pygame.K_SPACE: player_pos = [450, 663]

    pygame.display.flip()

  pygame.quit()