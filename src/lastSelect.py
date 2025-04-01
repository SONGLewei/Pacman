import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from visual.selectTheBestInTheJson import SelectTheBestInTheJson

if __name__ == "__main__":
    lastSelect = SelectTheBestInTheJson()
    lastSelect.run()
