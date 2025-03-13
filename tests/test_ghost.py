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
    
  # Up : Up first
  def testUp(self):
    self.ghost.x, self.ghost.y = 0, 300
    self.player.x, self.player.y = 0, 0  # Target tile is up
    self.ghost.setTargetTile(self.player.x, self.player.y)
    self.ghost.chooseDirection()
    print("Up Test")
    self.render()
    self.assertEqual(self.ghost.direction, "U")  # Up should be chosen first

  # Left : Left first
  def testLeft(self):
    self.ghost.x, self.ghost.y = 300, 0
    self.player.x, self.player.y = 0, 0  # Target tile is left
    self.ghost.setTargetTile(self.player.x, self.player.y)
    self.ghost.chooseDirection()
    print("Left Test")
    self.render()
    self.assertEqual(self.ghost.direction, "L")  # Left should be chosen first

  # Down : Down first
  def testDown(self):
    self.ghost.x, self.ghost.y = 0, 0
    self.player.x, self.player.y = 0, 300  # Target tile is down
    self.ghost.setTargetTile(self.player.x, self.player.y)
    self.ghost.chooseDirection()
    print("Down Test")
    self.render()
    self.assertEqual(self.ghost.direction, "D")  # Down should be chosen first

  # Right : Right first
  def testRight(self):
    self.ghost.x, self.ghost.y = 0, 0
    self.player.x, self.player.y = 300, 0  # Target tile is right
    self.ghost.setTargetTile(self.player.x, self.player.y)
    self.ghost.chooseDirection()
    print("Right Test")
    self.render()
    self.assertEqual(self.ghost.direction, "R")  # Right should be chosen first

  # Up-Left : Up first
  def testUpLeft(self):
    self.ghost.x, self.ghost.y = 300, 300
    self.player.x, self.player.y = 0, 0  # Target tile is diagonally up-left
    self.ghost.setTargetTile(self.player.x, self.player.y)
    self.ghost.chooseDirection()
    print("Up-Left Test")
    self.render()
    self.assertEqual(self.ghost.direction, "U")  # Up should be chosen first

  # Down-Left : Left first
  def testDownLeft(self):
    self.ghost.x, self.ghost.y = 300, 0
    self.player.x, self.player.y = 0, 300  # Target tile is diagonally down-left
    self.ghost.setTargetTile(self.player.x, self.player.y)
    self.ghost.chooseDirection()
    print("Down-Left Test")
    self.render()
    self.assertEqual(self.ghost.direction, "L")  # Left should be chosen first

  # Down-Right : Down first
  def testDownRight(self):
    self.ghost.x, self.ghost.y = 0, 0
    self.player.x, self.player.y = 300, 300  # Target tile is diagonally down-
    self.ghost.setTargetTile(self.player.x, self.player.y)
    self.ghost.chooseDirection()
    print("Down-Right Test")
    self.render()
    self.assertEqual(self.ghost.direction, "D")  # Down should be chosen first

  # Up-Right : Up first
  def testUpRight(self):
    self.ghost.x, self.ghost.y = 0, 300
    self.player.x, self.player.y = 300, 0  # Target tile is diagonally up-right
    self.ghost.setTargetTile(self.player.x, self.player.y)
    self.ghost.chooseDirection()
    print("Up-Right Test")
    self.render()
    self.assertEqual(self.ghost.direction, "U")  # Up should be chosen first

if __name__ == '__main__':
  unittest.main()