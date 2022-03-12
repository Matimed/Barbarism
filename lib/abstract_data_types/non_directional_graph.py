from typing import Any


class NonDirectionalGraph:
    """ A non-directional graph class that works with objects as node indices.
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


    def add_edge(self, *edges: tuple[Any, Any]):
        """ Add a link between two nodes.

            Receives:
                edge:<tuple> (node, node)
        """

        for edge in edges:
            self.add_node(edge[0], edge[1])
            
            if not edge[0] in self.nodes[edge[1]]:
                # Adds the nodes in the edge to the nodes dictionary.
                self.nodes[edge[0]].add(edge[1])
                self.nodes[edge[1]].add(edge[0])


    def remove_edge(self, *edges: tuple[Any, Any]):
        """ Remove a link between two nodes.

            Receives:
                edge:<tuple> (node, node)
        """

        self.verify_edge(*edges)

        for edge in edges:
            if edge[0] in self.nodes[edge[1]]:
                # Adds the nodes in the edge to the nodes dictionary.
                self.nodes[edge[0]].remove(edge[1])
                self.nodes[edge[1]].remove(edge[0])


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

    
    def edge_exist(self, edge: tuple[Any, Any]) -> bool:
        assert self.has_node(edge[0]) and self.has_node(edge[1]), \
            "The nodes in the edge must exist in the nodes dictionary."
        assert len(edge) == 2, "The edge must be a list with two nodes."

        return edge[0] in self.nodes[edge[1]]


    def set_adjacencies(self, node: Any, *adjacencies: Any):
        """ Overwrite all the adjacencies of a node.
        """

        self.remove_adjacency(node, self.nodes[node])
        self.add_adjacency(node, *adjacencies)

        
    def add_adjacency(self, node: Any, *adjacencies: Any):
        """ Create a connection between a node and all 
            the adjacent nodes that are passed as argument.
        """

        [self.add_edge((node, adjacency)) for adjacency in adjacencies]


    def remove_adjacency(self, node: Any, *adjacencies: Any):
        """ Remove all the connections between a node and 
            the adjacency nodes that are passed as argument.
        """

        [self.remove_edge(node, adjacency) for adjacency in adjacencies]

    
    def clear_nodes(self):
        """ Delete all the links between all the nodes.
        """

        for node in self.nodes:
            self.nodes[node].clear()

    
    def clear(self):
        """ Leave the graph empty.
        """
    
        self.nodes = dict()