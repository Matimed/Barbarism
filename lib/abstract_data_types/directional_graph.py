from typing import Any


class DirectionalGraph:
    """ A very simple directional graph class that works with objects as node indices.
    """

    def __init__(self):
        self.nodes = dict()


    def add_node(self, *nodes: Any):
        """ Add a node to the nodes dictionary.
        """

        [self.nodes.setdefault(node, set()) for node in nodes]


    def remove_node(self, node: Any):
        """ Remove a node from the nodes dictionary keys
            and from its adjacencies.
        """

        assert self.has_node(node), \
            "The node passed by argument doesn't exists."
            

        for n in self.nodes.pop(node):
            self.nodes[n].remove(node)


    def has_node(self, node: Any) -> Any:
        """ Returns if the node exist in the nodes dictionary.
        """

        return node in self.nodes

    
    def remove_empty_nodes(self):
        """ Removes all the nodes that not have any adjacencies.
        """

        [self.remove_node(node) for node in self.get_empty_nodes()]
                


    def get_empty_nodes(self):
        """ Returns all the nodes that not have any adjacencies.
        """

        return [node for node in self.nodes.keys() if not self.nodes[node]]


    def add_edge(self, node, *aimed_nodes):
        from lib.position import Position
        """ Add a link between two nodes.

            Receives:
                edge:<tuple> (node, node)
        """

        self.add_node(node)
        for aimed_node in aimed_nodes:
            if type(aimed_node) != Position: raise TypeError()
            self.add_node(aimed_node)

            self.nodes[node].add(aimed_node)


    def remove_edge(self, node, *aimed_nodes):
        """ Remove a link between two nodes.

            Receives:
                edge:<tuple> (node, node)
        """

        [self.edge_exist(node, aimed_node) for aimed_node in aimed_nodes]

        for aimed_node in aimed_nodes: self.nodes[node].remove(aimed_node)


    def verify_edge(self, *edges: tuple[Any, Any]):
        """ Verifies if an edge/s has two nodes.
        """

        for edge in edges:
            assert len(edge) == 2, "The edge must be a list with two node."


    def get_adjacencies(self, node: Any) -> set:
        """ Returns all the edges of a node.
        """

        assert self.has_node(node), \
            "The node passed by argument doesn't exists."

        return self.nodes[node]

    
    def edge_exist(self, node, aimed_node) -> bool:
        assert self.has_node(edge[0]) and self.has_node(edge[1]), \
            "The nodes in the edge must exist in the nodes dictionary."
        assert len(edge) == 2, "The edge must be a list with two nodes."

        return aimed_node[0] in self.nodes[node]


    def get_adjacencies(self, node):
        return self.nodes[node]


    def clear_nodes(self):
        """ Delete all the links between all the nodes.
        """

        for node in self.nodes:
            self.nodes[node].clear()

    
    def clear(self):
        """ Leave the graph empty.
        """
    
        self.nodes = dict()
