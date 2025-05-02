import numpy as np

class PacmanOfReseauNeuronOneLayer:
    def __init__(self):
        self.input_size = 25
        self.hidden_layer_size = 30
        self.output_size = 4

        self.network_weights = self.init_network()

    def getDecision(self, input_vector):
        action_probabilities = self.forward(self.network_weights, input_vector)
        direction_index = np.argmax(action_probabilities)
        directions = ["U", "D", "L", "R"]
        return directions[direction_index]

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def softmax(x):
        e = np.exp(x - np.max(x))
        return e / np.sum(e)

    def init_network(self):
        hidden_weights = np.random.uniform(-1, 1, size=(self.input_size, self.hidden_layer_size))
        output_weights = np.random.uniform(-1, 1, size=(self.hidden_layer_size, self.output_size))
        return [hidden_weights, output_weights]

    def forward(self, network_weights, input_vector):
        x = np.array(input_vector)
        hidden = self.relu(x.dot(network_weights[0]))
        output = self.softmax(hidden.dot(network_weights[1]))
        return output
