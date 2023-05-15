from visulaization import draw_network
import random

class Genome:
    class Node_gene:
        node_id_counter = 0

        def __init__(self, tag="", bias=0):
            self.id = self.node_id_counter
            Genome.Node_gene.node_id_counter += 1
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

        def __init__(self, start, end, tag="", weight=1):
            self.id = self.weight_id_counter
            Genome.Edge_gene.weight_id_counter += 1
            self.first_node = start
            self.second_node = end
            self.weight = weight
            self.tag = tag
            self.active = True
            genome.edges.append(self)

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
        self.add_all_static_nodes()

    def add_all_static_nodes(self):
        input_layer = []
        for i in range(self.number_inputs):
            input_node = self.Node_gene(tag="input")
            self.nodes.append(input_node)
            input_layer.append(input_node)
        self.layout.append(input_layer)

        output_layer = []
        for i in range(self.number_outputs):
            output_node = self.Node_gene(tag="output")
            self.nodes.append(output_node)
            output_layer.append(output_node)
        self.layout.append(output_layer)

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

    def get_connected_nodes(self, node):
        connected_nodes = []
        for x in self.edges:
            if x.get_start() is node:
                connected_nodes.append(x.get_end())

        return connected_nodes

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
        self.Edge_gene(start_node, end_node, tag)

    def split_edge(self, edge):
        if isinstance(edge, int):
            edge = genome.edges[edge]
        if not edge.active:
            return
        layer_distance = edge.get_end().get_layer() - edge.get_start().get_layer()
        if layer_distance == 1:
            edge.deactivate()
            start = edge.get_start()
            end = edge.get_end()
            middle_node = self.Node_gene()
            self.layout.insert(edge.get_end().get_layer(), [middle_node])
            self.Edge_gene(start, middle_node)
            self.Edge_gene(middle_node, end)

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

    def deactivate_random_edge(self):
        active_edges = []
        for x in self.edges:
            if x.active:
                active_edges.append(x)

    def mutate(self):
        pass


if __name__ == "__main__":
    genome = Genome(4, 1)
    for i in range(4):
        genome.add_random_edge()
        genome.add_random_edge()
        genome.split_random_edge()
    genome.draw_network()
