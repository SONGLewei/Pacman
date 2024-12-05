import os
import sys
import math
import pygame # type: ignore
from board import boards

WIDTH = 900
HEIGHT = 950
fps = 60
level = boards
wall_color = 'blue'
PI = math.pi

def drawBoard():
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
      elif level[i][j] == 2:
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
    
    for event in pygame.event.get():
      # Handle Quit event
      if event.type == pygame.QUIT: running = False

    pygame.display.flip()

  pygame.quit()