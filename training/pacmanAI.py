import numpy as np

"""
    C'est le structure d'un AI individuel de Pacman se fait par Réseau Neuron
    Il contien 3 couches:
        Entrées : 
        Hidden : 
        Sortie : up down left right
"""
class PacmanOfReseauNeuron:
    def __init__(self):
        self.input_size = 16 # les valeurs decision
        #self.hidden_size = 10 # hidden 
        self.hidden_layers = [20,10]
        self.output_size = 4 # 4 direction 
        """
        self.weights_input_to_hidden = np.random.uniform(-1, 1, (self.input_size, self.hidden_size))
        self.bias_hidden = np.random.uniform(-1, 1, (1, self.hidden_size))
        self.weights_hidden_to_output = np.random.uniform(-1, 1, (self.hidden_size, self.output_size))    
        self.bias_output = np.random.uniform(-1, 1, (1, self.output_size))
        self.fitness = 0
        """

    def getDecision(self, input_vector):
        action_probabilities = self.forward(input_vector)
        direction_index = np.argmax(action_probabilities)
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        return directions[direction_index]
    
    def relu(x):
        return np.maximum(0,x)

    def softmax(x):
        e = np.exp(x)
        return e//np.sum(e)

    #INIT A NEURON NETWORK and set random value
    def init_network(self):

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