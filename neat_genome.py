from visulaization import draw_network
import random
import math

softmax = lambda x: math.exp(x) / (math.exp(x) + 1)


class Genome:
    class Node_gene:
        node_id_counter = 0

        def __init__(self, parent_genome, tag="", bias=None):
            self.genome = parent_genome
            self.id = self.node_id_counter
            Genome.Node_gene.node_id_counter += 1

            self.genome.nodes.append(self)
            self.genome.node_values.append(0.0)
            self.genome.next_node_values.append(0.0)

            if bias is None:
                self.bias = Genome.get_random()
            else:
                self.bias = bias
            self.tag = tag

        def get_bias(self):
            return self.bias

        def get_id(self):
            return self.id

        def get_tag(self):
            return self.tag

        def get_layer(self):
            layout_index = genome.find_indexes_2d(genome.layout, self)
            return layout_index[0]

    class Edge_gene:
        weight_id_counter = 0

        def __init__(self, parent_genome,  start, end, tag="", weight=None):
            self.genome = parent_genome
            self.id = self.weight_id_counter
            Genome.Edge_gene.weight_id_counter += 1
            self.genome.edges.append(self)
            self.first_node = start
            self.second_node = end
            if weight is None:
                self.weight = Genome.get_random()
            else:
                self.weight = weight
            self.tag = tag
            self.active = True

        def get_weight(self):
            return self.weight

        def get_start(self):
            return self.first_node

        def get_end(self):
            return self.second_node

        def get_id(self):
            return self.id

        def get_tag(self):
            return self.tag

        def activate(self):
            self.active = True

        def deactivate(self):
            self.active = False

    def __init__(self, number_inputs, number_outputs):
        self.number_inputs = number_inputs
        self.number_outputs = number_outputs
        self.number_static_nodes = number_outputs + number_inputs
        self.layout = []
        self.nodes = []
        self.edges = []
        self.node_values = []
        self.next_node_values = []
        self.add_all_static_nodes()

    def add_all_static_nodes(self):
        input_layer = []
        for i in range(self.number_inputs):
            input_node = self.Node_gene(self, tag="input", bias=0.0)
            input_layer.append(input_node)
        self.layout.append(input_layer)

        output_layer = []
        for i in range(self.number_outputs):
            output_node = self.Node_gene(self, tag="output", bias=0.0)
            output_layer.append(output_node)
        self.layout.append(output_layer)

    @classmethod
    def get_random(cls, standard_deviation=1, mean_value=0):
        return random.normalvariate(mean_value, standard_deviation)

    def get_layout(self):
        return self.layout

    def draw_network(self):
        draw_network(self)

    @classmethod
    def find_indexes_2d(cls, array, item):
        for i, row in enumerate(array):
            for j, value in enumerate(row):
                if value == item:
                    return i, j
        return None

    def get_connected_nodes(self, node, with_weight=False):
        connected_nodes = []
        for x in self.edges:
            if x.active:
                if x.get_start() is node:
                    if with_weight:
                        connected_nodes.append([x.get_end(), x.get_weight()])
                    else:
                        connected_nodes.append(x.get_end())

        return connected_nodes

    def get_inputs(self, node):
        inputs = []
        for x in self.edges:
            if x.get_end() is node:
                inputs.append((x.get_start(), x))

    def get_free_connections(self, node):
        index, j = self.find_indexes_2d(self.layout, node)
        possible_connections = []
        occupied_connections = self.get_connected_nodes(node)

        if index+1 < len(self.layout):
            for i in self.layout[index+1:]:
                for n in i:
                    if n not in occupied_connections:
                        possible_connections.append(n)

        return possible_connections

    def add_edge(self, start_node, end_node, tag=""):
        self.Edge_gene(self, start_node, end_node, tag)

    # splits a given edge
    def split_edge(self, edge):
        if not edge.active:
            return
        layer_distance = edge.get_end().get_layer() - edge.get_start().get_layer()
        if layer_distance == 1:
            edge.deactivate()
            start = edge.get_start()
            end = edge.get_end()
            middle_node = self.Node_gene(self)
            self.layout.insert(edge.get_end().get_layer(), [middle_node])
            self.Edge_gene(self, start, middle_node)
            self.Edge_gene(self, middle_node, end)

    def add_random_edge(self):
        # get random node start_node
        random_layer_index = random.randint(0, len(self.layout)-2)  # excluding output-layer for start node
        random_start_node = random.choice(self.layout[random_layer_index])

        existing_connections = self.get_connected_nodes(random_start_node)

        # get random end_node
        free_connections = self.get_free_connections(random_start_node)
        if len(free_connections) > 0:
            random_end_node = random.choice(free_connections)
            self.add_edge(random_start_node, random_end_node)
        else:
            # TODO: recalling the function will lead to max recursion depth error eventually
            # self.add_random_edge()
            pass

    def split_random_edge(self):
        edge = random.choice(self.edges)
        self.split_edge(edge)

    def mutate_activation(self):
        active_edges = []
        for x in self.edges:
            if x.active:
                active_edges.append(x)

    def mutate(self):   # TODO
        pass

    def activate(self, x):
        if len(x) != self.number_inputs:
            raise ValueError("genome.activate() got wrong number of inputs")

        # setting input values
        for i, input in enumerate(x):
            self.node_values[i] = input

        # letting each node give its output to genome.next_node_values
        for i, node in enumerate(self.nodes):
            node_value = self.node_values[i]
            connected_nodes = self.get_connected_nodes(node, with_weight=True)
            for connected_node in connected_nodes:
                index = connected_node[0].get_id()
                self.next_node_values[index] += softmax(node_value * connected_node[1] + connected_node[0].get_bias())

        self.node_values = self.next_node_values.copy()
        for i, value in enumerate(self.next_node_values):
            self.next_node_values[i] = 0.0

        output = self.node_values[self.number_inputs:self.number_static_nodes]

        return output


if __name__ == "__main__":
    genome = Genome(1, 2)
    for i in range(2):
        genome.add_random_edge()
        # genome.add_random_edge()
        genome.split_random_edge()
    genome.draw_network()

    print(genome.activate([5]))
    print(genome.activate([5]))
    print(genome.activate([5]))
    print(genome.activate([5]))





