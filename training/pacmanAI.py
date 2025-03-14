import numpy as np


class PacmanAI:
    def __init__(self):
        self.input_size = 10 # les valeurs decision
        self.hidden_size = 10 # hidden 
        self.output_size = 4 # 4 direction 

        self.weights_input_to_hidden = np.random.uniform(-1, 1, (self.input_size, self.hidden_size))
        self.bias_hidden = np.random.uniform(-1, 1, (1, self.hidden_size))
        self.weights_hidden_to_output = np.random.uniform(-1, 1, (self.hidden_size, self.output_size))    
        self.bias_output = np.random.uniform(-1, 1, (1, self.output_size))
        self.fitness = 0

    def decide_action():
        return