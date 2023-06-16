import torch
import torch.nn as nn
import torch.nn.functional as f


class NEAT_Network(nn.Module):
    def __init__(self, genome):
        super().__init__(NEAT_Network, self)
        self.genome = genome

        # list with integer sizes of all hidden layers (e.g.: [3, 2, 1] )
        self.genome_shape = []
        for x in genome.layout:
            self.genome_shape.append(len(x))

        # self.genome_shape with included input and output layer
        self.genome_whole_shape = [genome.number_inputs, *self.genome_shape, genome.number_outputs]

        # creating pyTorch layers, with dimensions from self.genome_whole_shape
        self.layers = []
        for i, x in enumerate(self.genome_whole_shape[1:]):
            self.layers.append(nn.Linear(self.genome_whole_shape[i], x))

    def forward(self, x):
        if len(x) != len(self.genome_whole_shape[0]):
            raise ValueError("Network input does not match")

        node_value_list = [[[x, None] for x in i] for i in self.genome.layout]

        # setting values for input nodes
        for i, j in enumerate(node_value_list[0]):
            j[1] = x[i]

        # calculating values for all hidden nodes
        for layer in node_value_list[1:]:
            for node in layer:
                inputs = self.genome.get_inputs(node)
                out = 0
                for input in inputs:
                    index = self.genome.find_indexes_2d(self.genome.layout, input[0])
                    out += node_value_list[index[0]][index[1]][1] * input[1].get_weigth()
                node[1] = f.softmax(torch.Tensor(out))
        output_layer = node_value_list[-1]

        result = torch.zeros(self.genome_whole_shape[-1])
        for i, output_node in enumerate(node_value_list[-1]):
            result[i] = output_node[1]

        return result


if __name__ == "__main__":
    in_features = 5
    out_features = 10
    weights = torch.zeros((in_features, out_features))

    print(weights)
