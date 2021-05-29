

class NodeData:
    """
    This class represents the nodes in a weighted directed graph with the following calss variables:
        - info - the info stored in this node
        - tag - the tag assigned to this node
        - key - the unique key associated with this node
        - edges_from_node - a dictionary which stores all the edges which are directed from this node.
        for example, if there is an edge from this node to other node with weight of 7.3 then the dictionary
        will map the following {other_node_id : 7.3}.
        - edges_to_node - a dictionary which stores all the edges which are directed to this node.
        for example, if there is an edge from this node to other node with weight of 3.8 then the dictionary
        will map the following {other_node_id : 3.8}.
        - pos - a tuple representing the geographic position of this node.
    """

    def __init__(self, key: int, info: str = None, tag: float = 0, pos: tuple = None):
        """
        Constructor
        """
        self.info = info
        self.tag = tag
        self.key = key
        self.edges_from_node = {}
        self.edges_to_node = {}
        self.pos = pos

    def add_edge_from_node(self, ni_key: int, weight: float):
        """
        Adds an edge which is directed from this node to ni_key node (node -> other_node) by mapping
        the neighbor's key to the weight of the edge in edges_from_node dictionary
        @param ni_key - the key of the destination node
        @param weight - the weight of the edge
        @return
        """
        self.edges_from_node[ni_key] = weight

    def add_edge_to_node(self, ni_key: int, weight: float):
        """
        Adds an edge which is directed to this node from ni_key node (other_node -> node) by mapping
        the neighbor's key to the weight of the edge in edges_to_node dictionary
        @param ni_key - the key of the source node
        @param weight - the weight of the edge
        @return
        """
        self.edges_to_node[ni_key] = weight

    def get_edges_from_node(self) -> dict:
        """
        Returns a dictionary holding all the edges which are directed from this node by mapping them
        in pairs in the following way (ni_key, edge_weight), by returning the edges_from_node dictionary.
        @param
        @return a dictionary with all the edges from this node
        """
        return self.edges_from_node

    def get_edges_to_node(self) -> dict:
        """
        Returns a dictionary holding all the edges which are directed to this node by mapping them
        in pairs in the following way (ni_key, edge_weight), by returning the edges_to_node dictionary.
        @param
        @return a dictionary with all the edges to this node
        """
        return self.edges_to_node

    def get_edge_weight(self, ni_key: int) -> float:
        """
        Returns the weight of the edge from this node to ni_key (node -> ni_key) by retrieving it from
        the edges_from_node dictionary.
        @param
        @return the weight of the edge node->ni_key
        """
        return self.edges_from_node.get(ni_key)

    def get_key(self) -> int:
        """
        Returns the key of this node by returning self.key
        @param
        @return the key of this node
        """
        return self.key

    def get_info(self) -> str:
        """
        Returns the info stored in this node by returning self.info
        @param
        @return the info stored in this node
        """
        return self.info

    def set_info(self, info: str):
        """
        Sets this node's stored info to the provided info
        @param info
        @return
        """
        self.info = info

    def get_tag(self) -> float:
        """
        Returns the tag of this node by returning self.tag
        @param
        @return this node's tag
        """
        return self.tag

    def set_tag(self, tag: float):
        """
        Sets the tag of this node to the provided tag
        @param tag
        @return
        """
        self.tag = tag

    def get_pos(self) -> tuple:
        """
        Returns the geographic location of this node by returning self.pos
        @param
        @return this node's geographic location
        """
        return self.pos

    def set_pos(self, pos: tuple):
        """
        Sets this node's geographic location to the provided pos tuple
        @param pos
        @return
        """
        self.pos = pos


