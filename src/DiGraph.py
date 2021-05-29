from src.GraphInterface import GraphInterface
from src.node_data import NodeData


class DiGraph(GraphInterface):
    """
    This class implements GraphInterface which is a weighted directed graph with the following class variables:
        - nodes: a nodes dictionary which maps each node to his key int the following way -> {node_key: node},
        when each node stores his neighbors (from both incoming edges and outgoing edges)
        - mc: number of actions preformed on the the graph.
        - edge_size: number of edges in the graph
        *Note* - The implementation of the edges is in the NodeData class, when each node stores is
        incoming (directed to node) and outgoing (directed from node) edges.
    """

    def __init__(self):
        """
        Constructor
        """
        self.nodes = {}
        self.mc = 0
        self.edge_size = 0

    def v_size(self) -> int:
        """
        Returns the number of vertices in the graph
        @param
        @return number of vertices
        """
        return len(self.nodes)

    def e_size(self) -> int:
        """
        Returns the number of edges in the graph
        @param
        @return number of edges
        """
        return self.edge_size

    def get_all_v(self) -> dict:
        """
        Returns a dictionary containing all the vertices in the graph paired as (node_id : node_data)
        by return self.nodes
        @param
        @return dictionary of all the vertices
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        Returns a dictionary containing all the edges which are directed to the node (other_node -> node),
        which his key is the provided id1 parameter by returning the nodes get_edges_to_node().
        by return self.nodes
        @param id1 - key of the node
        @return dictionary of all the edges directed to the node, (empty dictionary if node not in graph).
        """
        if id1 not in self.nodes.keys():
            return {}
        return self.nodes.get(id1).get_edges_to_node()

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        Returns a dictionary containing all the edges which are directed from the node (node -> other_node),
        which his key is the provided id1 parameter by returning the nodes get_edges_from_node().
        by return self.nodes
        @param id1 - key of the node
        @return dictionary of all the edges directed from the node, (empty dictionary if node not in graph).
        """
        if id1 not in self.nodes.keys():
            return {}
        return self.nodes.get(id1).get_edges_from_node()

    def get_mc(self) -> int:
        """
        Returns the number of actions preformed on this graph by returning the mc class variable
        @param
        @return number of actions preformed on the graph
        """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Creates an edge from id1 to id2 (id1 ->id2) with the provided weight by using id1's add_edge_from_node()
        function and id2's add_edge_to_node() function.
        @param id1 - The id of the source node
        @param id2 - The id of the destination node
        @param weight - the weight of the edge
        @return True if and edge from id1 to id2 doesn't exists and a new one is created, false otherwise.
        """
        if id1 == id2 or weight < 0:
            return False
        elif (id1 not in self.nodes.keys()) or (id2 not in self.nodes.keys()):
            return False
        elif id2 in self.all_out_edges_of_node(id1).keys():
            return False
        else:
            self.nodes.get(id1).add_edge_from_node(id2, weight)
            self.nodes.get(id2).add_edge_to_node(id1, weight)
            self.mc += 1
            self.edge_size += 1
            return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph with the provided key by creating a new node (if doesn't already exits)
        and then adding it to nodes dictionary (key: node)
        @param node_id - the key of the node
        @param pos - the position of this node
        @return True if successfully created, false otherwise.
        """
        if node_id in self.nodes.keys():
            return False
        else:
            new_node = NodeData(key=node_id, pos=pos)
            self.nodes[node_id] = new_node
            self.mc += 1
            return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes the node associated with the provided node_id by first removing all the edges which are
        directed to him (other_node -> node), than removing all the node directed from him (node -> other_node)
        and them removing him from nodes dictionary.
        @param node_id - the node's key
        @return True if successfully removed, false otherwise.
        """
        if node_id not in self.nodes.keys():
            return False
        else:
            neighbors_to_node = []
            neighbors_to_node.extend(self.all_in_edges_of_node(node_id).keys())
            if neighbors_to_node:
                for ni_key in neighbors_to_node:
                    self.remove_edge(ni_key, node_id)
            neighbors_from_node = []
            neighbors_from_node.extend(self.all_out_edges_of_node(node_id).keys())
            if neighbors_from_node:
                for ni_key in neighbors_from_node:
                    self.remove_edge(node_id, ni_key)
            del self.nodes[node_id]
            self.mc += 1
            return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes the edge from node_id1 to node_id2 by removing node_id1 from the to_nodes dictionary
        of node_id2 and removing node_id2 from the from_node dictionary of node_id1
        @param node_id1 - the source node
        @param node_id2 - the destination node
        @return True if successfully removed, false otherwise.
        """
        if node_id1 == node_id2:
            return False
        elif node_id1 not in self.nodes.keys() or node_id2 not in self.nodes.keys():
            return False
        elif node_id2 not in self.all_out_edges_of_node(node_id1).keys():
            return False
        else:
            del self.nodes.get(node_id1).get_edges_from_node()[node_id2]
            del self.nodes.get(node_id2).get_edges_to_node()[node_id1]
            self.edge_size -= 1
            self.mc += 1
            return True

    def __eq__(self, other):
        for node_key in self.nodes.keys():
            if node_key not in other.nodes.keys():
                return False
            else:
                if self.all_out_edges_of_node(node_key) != other.all_out_edges_of_node(node_key):
                    return False
        return True




