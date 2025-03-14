# main.py
from controller.game import Game

if __name__ == "__main__":
  game = Game()
  game.startGame()

  #在边界被吃掉的时候回不了家卡住不动
  #解决方案：死亡状态下在原地等5s不动直接传送回家
  #死亡之后速度变慢
  #不能加速否则不好计算正好在砖块