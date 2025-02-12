import unittest
import sys
import os
import pygame # type: ignore
import platform

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from elements.ghost import Ghost
from elements.entity import Entity

class MockPlayer(Entity):
  def __init__(self, x, y, direction=None, last_direction=None):
    super().__init__(x, y)
    self.direction = direction
    self.last_direction = last_direction

  def render(self, screen):
    pygame.draw.circle(screen, 'yellow', (self.x + 15, self.y + 15), 15)

class TestGhost(unittest.TestCase):
  def setUp(self):
    self.ghost = Ghost(0, 0, "red")
    self.player = MockPlayer(0, 0)

    pygame.display.init()
    self.screen = pygame.display.set_mode([900, 900])
    pygame.display.set_caption("Test Ghost Movement")
    self.clock = pygame.time.Clock()

  def tearDown(self):
    pygame.quit()

  def render(self):
    self.screen.fill('black')
    self.ghost.render(self.screen)
    self.player.render(self.screen)
    pygame.display.flip()

    # Wait for spacebar press to continue
    waiting = True
    while waiting:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          waiting = False

  # def test_smallest_distance_chosen(self):
  #   self.ghost.x, self.ghost.y = 0, 0
  #   self.player.x, self.player.y = 600, 0  # Target tile is to the right
  #   self.ghost.move(self.player)
  #   print("Smallest Distance Test")
  #   self.render()
  #   self.assertEqual(self.ghost.direction, "R")
    
  # Up-Left : Up first
  def testUpLeft(self):
    self.ghost.x, self.ghost.y = 300, 300
    self.player.x, self.player.y = 0, 0  # Target tile is diagonally up-left
    self.ghost.target(self.player.x, self.player.y)
    print("Up-Left Test")
    self.render()
    self.assertEqual(self.ghost.direction, "U")  # Up should be chosen first

  # Down-Left : Left first
  def testDownLeft(self):
    self.ghost.x, self.ghost.y = 300, 0
    self.player.x, self.player.y = 0, 300  # Target tile is diagonally down-left
    self.ghost.target(self.player.x, self.player.y)
    print("Down-Left Test")
    self.render()
    self.assertEqual(self.ghost.direction, "L")  # Left should be chosen first

  # Down-Right : Down first
  def testDownRight(self):
    self.ghost.x, self.ghost.y = 0, 0
    self.player.x, self.player.y = 300, 300  # Target tile is diagonally down-
    self.ghost.target(self.player.x, self.player.y)
    print("Down-Right Test")
    self.render()
    self.assertEqual(self.ghost.direction, "D")  # Down should be chosen first

  # Up-Right : Up first
  def testUpRight(self):
    self.ghost.x, self.ghost.y = 0, 300
    self.player.x, self.player.y = 300, 0  # Target tile is diagonally up-right
    self.ghost.target(self.player.x, self.player.y)
    print("Up-Right Test")
    self.render()
    self.assertEqual(self.ghost.direction, "U")  # Up should be chosen first
    
  # Up-Left : Up first
  def testUpLeftFrighten(self):
    self.ghost.x, self.ghost.y = 300, 300
    # Target tile is diagonally up-left
    self.player.x, self.player.y = 0, 0
    self.ghost.frighten()
    self.ghost.frightened(self.player)
    print("Up-Left Test")
    self.render()
    self.assertEqual(self.ghost.direction, "D")

  # Down-Left : Left first
  def testDownLeftFrighten(self):
    self.ghost.x, self.ghost.y = 300, 0
    # Target tile is diagonally down-left
    self.player.x, self.player.y = 0, 300  
    self.ghost.frighten()
    self.ghost.frightened(self.player)
    print("Down-Left Test")
    self.render()
    self.assertEqual(self.ghost.direction, "U") 

  # Down-Right : Down first
  def testDownRightFrighten(self):
    self.ghost.x, self.ghost.y = 0, 0
    # Target tile is diagonally down-right
    self.player.x, self.player.y = 300, 300  
    self.ghost.frighten()
    self.ghost.frightened(self.player)
    print("Down-Right Test")
    self.render()
    self.assertEqual(self.ghost.direction, "U") 

  # Up-Right : Up first
  def testUpRightFrighten(self):
    self.ghost.x, self.ghost.y = 0, 300
    # Target tile is diagonally up-right
    self.player.x, self.player.y = 300, 0
    self.ghost.frighten()
    self.ghost.frightened(self.player)
    print("Up-Right Test")
    self.render()
    self.assertEqual(self.ghost.direction, "L")

if __name__ == '__main__':
  unittest.main()