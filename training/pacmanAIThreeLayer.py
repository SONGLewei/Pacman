import numpy as np

class PacmanOfReseauNeuronThreeLayer:
    def __init__(self):
        self.input_size = 25
        self.hidden_layers = [30, 20, 10]
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
        layers = []
        prev_dim = self.input_size

        for h in self.hidden_layers:
            layers.append(np.random.uniform(-1, 1, size=(prev_dim, h)))
            prev_dim = h

        layers.append(np.random.uniform(-1, 1, size=(prev_dim, self.output_size)))
        return layers

    def forward(self, network_weights, input_vector):
        x = np.array(input_vector)

        for W in network_weights[:-1]:
            x = self.relu(x.dot(W))

        out = x.dot(network_weights[-1])
        return self.softmax(out)
