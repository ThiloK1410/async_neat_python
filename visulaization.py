import graphviz


def draw_network(network):
    graph = graphviz.Digraph("Network")
    graph.attr(rankdir="LR")

    # add input layer
    with graph.subgraph(name="input") as c:
        c.attr(label="Input Layer")
        c.attr(color="blue")
        c.attr(rank="same")
        for i in range(network.number_inputs):
            c.node(name=str(network.nodes[i].get_id()),
                   label=f"id:{network.nodes[i].get_id()} | {network.nodes[i].get_tag()}")

    # add all hidden nodes
    for i in network.nodes[network.number_static_nodes:]:
        graph.node(name=f"{i.get_id()}", label=f"id:{i.get_id()}\nbias:{i.get_bias():.3f}")

    # add output layer
    with graph.subgraph(name="output") as c:
        c.attr(label="Output Layer", rank="same")
        for i in range(network.number_inputs, network.number_static_nodes):
            c.node(name=str(network.nodes[i].get_id()),
                   label=f"id:{network.nodes[i].get_id()} | {network.nodes[i].get_tag()}",
                   rank="same")

    graph.edge(tail_name="1", head_name=f"{network.number_inputs}", style="invis")

    for i in network.edges:
        if i.active:
            weight = i.get_weight()
            graph.edge(str(i.get_start().get_id()),
                       str(i.get_end().get_id()),
                       label=f"id:{i.get_id()} | weight:{weight:.3f}")

    graph.render("network.gv", view=True)
    # print(graph.source)


if __name__ == "__main__":
    dot = graphviz.Digraph("firstGraph")
    dot.attr(rankdir="LR")
    with dot.subgraph(name="layer_0") as c:
        c.node("1", "BIAS")
        c.node("2", "otherBIAS")
    with dot.subgraph(name="layer_1") as c:
        c.node("3", "other1")
        c.node("4", "other2")
    #dot.edges(["13", "14", "23", "24"])

    dot.render("firstGraph.gv", view=True)
