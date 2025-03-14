import random

class RandomAI:
    def decide_action(self, player, ghosts, static_entities):
        directions = ["R", "L", "U", "D"]
        random.shuffle(directions)
        for d in directions:
            if player.canMove(d):
                return d
        return "STOP"