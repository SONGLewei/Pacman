import numpy as np
#import torch
"""
    C'est le structure d'un AI individuel de Pacman se fait par Réseau Neuron
    Il contien 3 couches:
        Entrées : 
        Hidden : 
        Sortie : up down left right
"""
class PacmanOfReseauNeuron:
    def __init__(self):
        self.input_size = 22 # les valeurs decision
        self.hidden_layers = [20,10]
        self.output_size = 4 # 4 direction 
        self.network_weights = self.init_network()

    def getDecision(self, input_vector):
        action_probabilities = self.forward(self.network_weights, input_vector)
        direction_index = np.argmax(action_probabilities)
        directions = ["U", "D", "L", "R"]
        return directions[direction_index]
    
    @staticmethod
    def relu(x):
        return np.maximum(0,x)
    
    @staticmethod
    def softmax(x):
        e = np.exp(x - np.max(x)) 
        return e / np.sum(e)

    def init_network(self):
        """
        Init a neuron network and set random value
        [
            17 rows * 20 columns,
            20 rows * 10 columns,
            10 rows * 4  columns
        ]

        """
        # FOR each floor, creat matrix
        layers = []
        prev_dim = self.input_size

        for h in self.hidden_layers:
            layers.append(np.random.uniform(-1,1,size=(prev_dim,h)))
            prev_dim = h
        
        # OUTPUT
        layers.append(np.random.uniform(-1, 1, size=(prev_dim, self.output_size)))
        return layers


    def forward(self,network_weights, input_vector):
        # Handle input
        x = np.array(input_vector)
        # HIDDEN
        for idx, W in enumerate(network_weights[:-1]):
            x = x.dot(W)
            # Use relu in the hidden
            x = self.relu(x)
        # OUT
        out = x.dot(network_weights[-1])
        out = self.softmax(out)
        return out